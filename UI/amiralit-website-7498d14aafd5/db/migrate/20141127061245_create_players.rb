class CreatePlayers < ActiveRecord::Migration
  def change
    create_table :players do |t|
      t.string :name
      t.boolean :twitter
      t.boolean :facebook

      t.timestamps
    end
  end
end
