json.array!(@tasks) do |task|
  json.extract! task, :id, :name, :frequency, :month, :day_of_week, :day_of_month, :hour, :command
  json.url task_url(task, format: :json)
end
