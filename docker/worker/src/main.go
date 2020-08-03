package main

import (
	"encoding/json"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/kelseyhightower/envconfig"
	"github.com/pkg/errors"
	log "github.com/sirupsen/logrus"
	"golang.org/x/sync/errgroup"
	"runtime"
	"strings"
	"time"
)

type Config struct {
	SqsAwsRegion   string `default:"us-east-1" split_words:"true"`
	SqsEndPointUrl string `default:"http://127.0.0.1:9324" split_words:"true"`
	SqsQueueUrl    string `default:"http://127.0.0.1:9324/queue/test" split_words:"true"`
}

func initLog() {
	log.SetReportCaller(true)
	log.SetFormatter(&log.TextFormatter{
		FullTimestamp: true,
		CallerPrettyfier: func(f *runtime.Frame) (string, string) {
			filepath := strings.Split(f.File, "/")
			return "", fmt.Sprintf(" %s:%d", filepath[len(filepath)-1], f.Line)
		},
	})
}

type SqsClient struct {
	svc *sqs.SQS
}

func NewSqsClient(region, endpoint string) *SqsClient {
	sess, err := session.NewSession(
		&aws.Config{
			Region:   aws.String(region),
			Endpoint: aws.String(endpoint),
		},
	)
	if err != nil {
		log.Error("aws session new error")
		panic(err)
	}

	svc := sqs.New(sess)
	return &SqsClient{
		svc: svc,
	}
}

func (c *SqsClient) ReceiveMessage(queueUrl string) (*sqs.ReceiveMessageOutput, error) {
	params := &sqs.ReceiveMessageInput{
		AttributeNames:      []*string{aws.String("All")},
		QueueUrl:            aws.String(queueUrl),
		MaxNumberOfMessages: aws.Int64(10),
		WaitTimeSeconds:     aws.Int64(10),
	}
	return c.svc.ReceiveMessage(params)
}

func (c *SqsClient) DeleteMessage(msg *sqs.Message, queueUrl string) error {
	params := &sqs.DeleteMessageInput{
		QueueUrl:      aws.String(queueUrl),
		ReceiptHandle: aws.String(*msg.ReceiptHandle),
	}
	_, err := c.svc.DeleteMessage(params)

	if err != nil {
		log.Error(err)
		return errors.WithStack(err)
	}
	return nil
}

type SqsClientI interface {
	ReceiveMessage(string) (*sqs.ReceiveMessageOutput, error)
	DeleteMessage(*sqs.Message, string) error
}

func Subscribe(sqsClient SqsClientI, goenv Config) error {
	// sqs get MQ
	messages, err := sqsClient.ReceiveMessage(goenv.SqsQueueUrl)
	if err != nil {
		// キューと接続できない時にスリープする
		time.Sleep(time.Second * 5)
		log.Error("sqs receive message error")
		return errors.WithStack(err)
	}
	log.Debug(messages.Messages)

	if len(messages.Messages) == 0 {
		log.Info("sqs receive message is empty")
		return nil
	}
	// sqs message数ほどgoroutineを実行
	var eg errgroup.Group

	for _, m := range messages.Messages {
		// 非同期実行
		msg := m
		eg.Go(func() error {
			var queueRes QueueMessage
			err := json.Unmarshal([]byte(*msg.Body), &queueRes)
			if err != nil {
				log.Error("sqs receive message json unmarshal error")
				return errors.WithStack(err)
			}
			// キーが存在しない場合にUnmarshalするとvalueで0が返ってくる
			if queueRes.Id == 0 {
				log.Error("sqs receive message json unmarshal value zero")
				return fmt.Errorf("err: json unmarshal queue is %+v", queueRes)
			}

			// queueの値を使った処理
			log.Infof("main process Id is %d", queueRes.Id)

			err = sqsClient.DeleteMessage(msg, goenv.SqsQueueUrl)
			if err != nil {
				log.Error("sqs delete message error")
				return errors.WithStack(err)
			}
			log.Debug(msg)
			log.Info("sqs message deleted")
			return nil
		})
	}

	// goroutineで発生したエラーを返却
	if err := eg.Wait(); err != nil {
		log.Error(err.Error())
		return errors.WithStack(err)
	}

	log.Info("sqs receive message complete")
	return nil
}

type QueueMessage struct {
	Id int `json:"id"`
}

func main() {
	initLog()
	// 環境変数から定数取得
	var goenv Config
	envconfig.Process("", &goenv)

	sqsClient := NewSqsClient(goenv.SqsAwsRegion, goenv.SqsEndPointUrl)

	for {
		if err := Subscribe(sqsClient, goenv); err != nil {
			log.Error(err.Error())
		}
	}
}
