require 'aws-sdk'

loop do
  begin
    sqscli = Aws::SQS::Client.new(
      region:            ENV['SQS_AWS_REGION'],
      endpoint:          ENV['SQS_END_POINT_URL'],
      access_key_id:     ENV['SQS_ACCESS_KEY'],
      secret_access_key: ENV['SQS_SECRET_KEY'],
    )
    sqscli.create_queue(queue_name: ENV['SQS_QUEUE_NAME'])
    puts "Queue created successfully `queue/#{ENV['SQS_QUEUE_NAME']}`."
    break
  rescue
    puts 'Server not initialized, please try again.'
    puts '...waiting...'
    sleep 1
  end
end
