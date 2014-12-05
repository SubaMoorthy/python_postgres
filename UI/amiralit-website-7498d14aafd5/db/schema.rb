# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20141201012319) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "facebook", id: false, force: true do |t|
    t.text    "full_name"
    t.text    "team"
    t.text    "facebook_id"
    t.decimal "likes"
    t.decimal "talking_about"
    t.decimal "post_count"
    t.text    "post_ids",      array: true
  end

  create_table "facebook_posts", id: false, force: true do |t|
    t.text    "post_id"
    t.text    "status"
    t.decimal "likes"
    t.decimal "comment_count"
    t.text    "comments",      array: true
  end

  create_table "job_run", primary_key: "job_run_id", force: true do |t|
    t.integer  "task_id"
    t.datetime "start_time"
    t.datetime "end_time"
    t.string   "status",     limit: 64
  end

  create_table "nasl", id: false, force: true do |t|
    t.string "player_name",  limit: 30
    t.string "current_team", limit: 30
    t.string "goals",        limit: 10
  end

  create_table "player", id: false, force: true do |t|
    t.text    "first_name"
    t.text    "middle_name"
    t.text    "last_name"
    t.text    "full_name",                  null: false
    t.string  "gender",           limit: 6
    t.text    "source",                     null: false
    t.text    "team_name"
    t.text    "division"
    t.text    "conference"
    t.decimal "goals"
    t.float   "height"
    t.text    "heightin"
    t.decimal "weight"
    t.decimal "yellow"
    t.decimal "red"
    t.decimal "assist"
    t.decimal "duplicate"
    t.text    "date_of_birth"
    t.decimal "age"
    t.text    "seasons"
    t.text    "positions"
    t.text    "position_1"
    t.text    "sequence_val"
    t.text    "person_key"
    t.text    "jersey"
    t.decimal "register_num"
    t.decimal "num"
    t.text    "last_team"
    t.text    "approved"
    t.text    "nick_name"
    t.decimal "games_played"
    t.decimal "game_starts"
    t.decimal "sub_ins"
    t.decimal "points"
    t.decimal "shots"
    t.decimal "shots_on_target"
    t.decimal "foul_committed"
    t.decimal "foul_suffered"
    t.decimal "fouls"
    t.text    "pending"
    t.decimal "minutes"
    t.decimal "saves"
    t.decimal "goals_conceded"
    t.text    "country"
    t.decimal "win"
    t.decimal "lose"
    t.decimal "draw"
    t.text    "status"
    t.decimal "r_shots_on_goals"
    t.boolean "twitter"
    t.boolean "facebook"
  end

  create_table "players", force: true do |t|
    t.string   "name"
    t.boolean  "twitter"
    t.boolean  "facebook"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "tasks", force: true do |t|
    t.string   "name"
    t.string   "frequency"
    t.integer  "month"
    t.integer  "day_of_week"
    t.integer  "day_of_month"
    t.integer  "hour"
    t.string   "command"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "folder"
  end

  create_table "team", id: false, force: true do |t|
    t.text    "team_name",                 null: false
    t.decimal "goals"
    t.decimal "fouls"
    t.decimal "yellow"
    t.decimal "red"
    t.text    "source",                    null: false
    t.decimal "duplicate"
    t.decimal "games_played"
    t.decimal "shots"
    t.decimal "points"
    t.decimal "wins"
    t.decimal "losses"
    t.decimal "ties"
    t.decimal "games_for"
    t.decimal "games_against"
    t.decimal "home_wins"
    t.decimal "home_losses"
    t.decimal "home_ties"
    t.decimal "home_games_for"
    t.decimal "home_games_against"
    t.decimal "away_wins"
    t.decimal "away_losses"
    t.decimal "away_ties"
    t.decimal "away_games_for"
    t.decimal "away_games_against"
    t.text    "team_id"
    t.text    "tournament"
    t.decimal "home_games_played"
    t.decimal "home_points"
    t.decimal "away_games_played"
    t.decimal "away_points"
    t.decimal "goal_difference"
    t.decimal "home_goal_difference"
    t.decimal "away_goal_difference"
    t.decimal "streaks"
    t.decimal "home_streaks"
    t.decimal "away_streaks"
    t.decimal "r_games_played"
    t.decimal "r_goals"
    t.decimal "r_assists"
    t.decimal "r_shots"
    t.decimal "r_shots_on_goals"
    t.decimal "r_fouls_committed"
    t.decimal "r_fouls_suffered"
    t.decimal "r_offsides"
    t.decimal "r_corner_kick"
    t.decimal "r_penality_kick_goals"
    t.decimal "r_penality_kick_attempts"
    t.decimal "p_games_played"
    t.decimal "p_goals"
    t.decimal "p_assists"
    t.decimal "p_shots"
    t.decimal "p_shots_on_goals"
    t.decimal "p_fouls_committed"
    t.decimal "p_fouls_suffered"
    t.decimal "p_offsides"
    t.decimal "p_corner_kick"
    t.decimal "p_penality_kick_goals"
    t.decimal "p_penality_kick_attempts"
    t.text    "largest_attendance"
    t.text    "lowest_attendance"
    t.text    "most_home_goals"
    t.text    "most_away_goals"
    t.text    "largest_margin_of_victory"
    t.text    "average_attendance"
    t.text    "aggregated_attendance"
    t.text    "longest_losing_streak"
    t.text    "longest_unbeaten_streak"
    t.text    "longest_winless_streak"
    t.text    "longest_winning_streak"
    t.text    "scorer",                                 array: true
    t.text    "assister",                               array: true
    t.text    "discs",                                  array: true
    t.text    "players",                                array: true
    t.decimal "year"
  end

  create_table "test_py", id: false, force: true do |t|
    t.integer "id"
  end

  create_table "twitter", id: false, force: true do |t|
    t.text    "full_name"
    t.text    "screen_name"
    t.text    "twitter_id"
    t.date    "created"
    t.text    "description"
    t.decimal "num_of_followers"
    t.text    "num_of_tweets"
    t.text    "website_url"
  end

  create_table "twitter_tweets", id: false, force: true do |t|
    t.text "full_name"
    t.text "tweet_id"
    t.text "tweet"
    t.date "created"
    t.text "retweets"
    t.text "retweet_count"
    t.text "tweet_source"
  end

end
