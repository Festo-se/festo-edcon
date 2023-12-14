from edcon.gui.costumtablemodel import CostumTableModel

class CostumTableCsv():
    def __init__(self, data, tblPnuList):
        super().__init__()

        file_path = data
        self.table = tblPnuList

        # create table
        table = []

        # open and read file
        with open(file_path, "r") as file:
          content = file.read()

          # Split content into lines.
          lines = content.split("\n")

        # Iterate through each row
        for line in lines:
          # Split column values 2
          columns = line.split(";")
    
          # Add the column values to the current row in the table
          table.append(columns)
    
          # If a new line begins in the file, add a new row to the table
          if len(columns) == 1:
            table.append([])

        self.model = CostumTableModel(table)
        self.table.setModel(self.model)