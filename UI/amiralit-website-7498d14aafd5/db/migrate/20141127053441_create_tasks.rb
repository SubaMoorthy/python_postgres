class CreateTasks < ActiveRecord::Migration
  def change
    create_table :tasks do |t|
      t.string :name
      t.string :frequency
      t.integer :month
      t.integer :day_of_week
      t.integer :day_of_month
      t.integer :hour
      t.string :command

      t.timestamps
    end
  end
end
