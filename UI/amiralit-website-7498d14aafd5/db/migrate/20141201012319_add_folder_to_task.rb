class AddFolderToTask < ActiveRecord::Migration
  def change
    add_column :tasks, :folder, :string
  end
end
