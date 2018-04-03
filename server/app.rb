require 'sinatra'

get '/' do
  'Hello from the server!'
end

post '/test' do
  received = params[:message]
  if received == 'hello_from_extension'
    { successful: true, message: 'It worked!' }.to_json
  else
    { successful: false, message: "I didn't get the expected message" }.to_json
  end
end