import sys
import csv
import time
import os
import logging

input_filepath = sys.argv[1]
output_filepath = sys.argv[2]
log_filepath = os.path.dirname(output_filepath) + '/app.log'

#
# Function to setup logger
#
def setup_logger(log_filepath):
    logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    return logging


#
# Function to validate if input file exits and is readable and verify output file in case it's incorrect
#
def validating_setup(input_filepath, output_filepath):
    logging.info('[Start] Validating File Setup')
    try:
        os.path.exists(input_filepath)
        logging.info('[Attr] Input File Path --> input_filepath: ' + input_filepath)
    except OSError:
        logging.error('[Error] Input file path has some issues. Please check!')
        quit()
    try:
        logging.info('[Attr] Output File Path --> output_filepath: ' + output_filepath)
        with open(output_filepath, 'w'):
            pass
    except OSError:
        logging.error('[Error] Output file path has some issues. Please check!')
        quit()
    logging.info('[Done] Validating setup')



class InventoryItem(object):
    """An InventoryItem is an item in inventory list. InventoryItem have the
            following properties:

            Attributes:
                drug_name: A string representing the drug's name.
                total_cost: (req float) A float tracking the total cost of drug name entries in order list.
                prescriber_set: Set of Unique Prescriber Name's who have been prescribed the medicines.
                id: Id from order list (not much useful currently but can be in future)
    """

    def __init__(self, id, prescriber_name, drug_name, total_cost):
        """Return a InventoryItem object whose drug_name is *drug_name* and starting
                total_cost is *total_cost*, prescriber_set has prescriber_name added.
                Id for now is *Id*"""
        self.id = id
        self._prescriber_set = set([prescriber_name.upper()])
        self.drug_name = drug_name
        self.total_cost = total_cost
        if (prescriber_name == '_'):
            raise ValueError('ValueError prescriber_name in the input_file for *this* line is not a string.')

    @property
    def drug_name(self):
        return self._drug_name

    @drug_name.setter
    def drug_name(self, value):
        if value:
            self._drug_name = value.upper()
        else:
            raise ValueError('ValueError drug_name in the input_file for *this* line is not a string.')

    @property
    def total_cost(self):
        return self._total_cost

    @total_cost.setter
    def total_cost(self, value):
        try:
            self._total_cost = float(value)
        except:
            raise ValueError('ValueError total_cost in the input_file for *this* line is not numerical.')

    @property
    def prescriber_set(self):
        return self._prescriber_set

    @prescriber_set.setter
    def prescriber_set(self, value):
#        prescriber_name = next(iter(value))
#        print('prescriber_name: ' + prescriber_name.upper())
        if not (prescriber_name == '_'):
            pass
        else:
            logging.error('[Error] ValueError in prescriber_name value while creating InventoryItem object')
            raise ValueError('prescriber_name in the input_file for *this* line is not a string. Skipping it until fixed.')

    def __str__(self):
        return "drug_name: " + self.drug_name + ", prescriber_set: " + str(
            self.prescriber_set) + ", total_cost: " + str(self.total_cost) + ", sort_field: " + self.temp_sort_field


class Inventory(object):
    """An Inventory is an inventory of all drug_name, total_cost of drug_name prescribed with
                total_cost to all prescribers. Inventory have the following properties:

                Attributes:
                    inventory_dict: A dictionary of all inventory_item objects with following key-value pair:
                                    Key: drug_name
                                    Value: inventory_item object
    """

    def __init__(self):
        """Return a Inventory object with empty inventory dictionary ."""
        self.inventory_dict = {}

    def list_top(self):
        """Writes list of top sorted drub_names to output_path file location.
            format: drug_name, num_unique_prescribers, total_cost"""
        logging.info('[Starting] Generating (sorting) top inventory list')
        inventory_list = list(self.inventory_dict.values())

        result_list = sorted(inventory_list, key=lambda x: (x.total_cost, x.drug_name), reverse=True)
        try:
            output_file_handler = open(output_filepath, mode="w")
            for i in result_list:
                output_file_handler.write(
                    '\'' + str(i.drug_name) + '\'' + ',' + str(len(i.prescriber_set)) + ',' + str(i.total_cost) + '\n')
            output_file_handler.close()
        except OSError:
            logging.error('[Error] Output file path has some issues. Please check!')
            quit()

        logging.info('[Done] Generated top inventory list file at output_file_path')


    def add_to_inventory(self, inventoryItem):
        """Adds inventoryItem to inventory_dictionary based on following logic:
            if drug_name unique: update attr of inventoryItem associated with it (total_cost & add prescriber_name to prescriber_set)
            else: add drug_name to dictionary: with new inventoryItem object instance"""
        uniq_prescriber_name = next(iter(inventoryItem.prescriber_set))

        if str(inventoryItem.drug_name) in self.inventory_dict:
            if (uniq_prescriber_name not in self.inventory_dict[inventoryItem.drug_name].prescriber_set):
                self.inventory_dict[inventoryItem.drug_name].prescriber_set.add(uniq_prescriber_name)
                self.inventory_dict[inventoryItem.drug_name].total_cost = float(
                    self.inventory_dict[inventoryItem.drug_name].total_cost) + float(inventoryItem.total_cost)
                self.inventory_dict[inventoryItem.drug_name].num_prescriber = len(
                    self.inventory_dict[inventoryItem.drug_name].prescriber_set)
            else:
                self.inventory_dict[inventoryItem.drug_name].total_cost = float(
                    self.inventory_dict[inventoryItem.drug_name].total_cost) + float(inventoryItem.total_cost)
        else:
            self.inventory_dict[inventoryItem.drug_name] = inventoryItem


def main():

    logging = setup_logger(log_filepath)
    validating_setup(input_filepath, output_filepath)

    inventory = Inventory()

    start_time = time.clock()

    line_number = 0
    logging.info('[Starting] To read through the input file')
    with open(input_filepath) as input_list:
        for line in input_list:
            for parsed_line in csv.reader([line], skipinitialspace=True):
                line_number += 1
                try:
                    prescriber_name = parsed_line[1] + '_' + parsed_line[2]

                    inventoryItem = InventoryItem(parsed_line[0], prescriber_name, parsed_line[3], parsed_line[4])
                    inventory.add_to_inventory(inventoryItem)
                except Exception as e:
                    logging.error('[Error] Line_number: ' + str(line_number) + ', Exception: ' + str(e))

    logging.info('[Done] Reading through the input file')

    inventory.list_top()

    elapse_time = time.clock() - start_time
    logging.info('[Perf] Time elapsed for generating pharma list from orders_list: ' + str(elapse_time) + 'ms')  # CPU seconds elapsed (floating point)


main()
