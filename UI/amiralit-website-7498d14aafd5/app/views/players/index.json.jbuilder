json.array!(@players) do |player|
  json.extract! player, :id, :name, :twitter, :facebook
  json.url player_url(player, format: :json)
end
