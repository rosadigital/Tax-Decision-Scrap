from selenium import webdriver
import pandas as pd

class Main():
    def run(self):
        # opening page
        url = 'https://acordaos.economia.gov.br/solr/acordaos2/browse/'
        driver = webdriver.Chrome('chromedriver')
        driver.get(url)

        # verifying decisions per page
        result_document = driver.find_elements_by_xpath('//*[@id="content"]/div[5]/div')
        divs_of_table = len(result_document)

        # verifying amount of fields to be searched
        all_fields_on_page = driver.find_elements_by_xpath("//*[@id='content']/div[5]/div//strong")
        fields = []
        for field_on_page in all_fields_on_page:
            fields.append(field_on_page.text)

        # removing duplicate fields names from this list
        fields = list(dict.fromkeys(fields))
        fields = [elements_in_fields.strip(':') for elements_in_fields in fields] #removing semicolon from elements

        # creating list structure for future dataframe
        df_decision = []

        for field in fields:
            field += ":" # necessary complement for searching on page by xpath

            # creating columns for each field
            df_decision_column = []

            # saving data in columns
            for div in range(1, divs_of_table + 1):
                try:
                    # On DOM, searching parent element of data (if it exists, driver navigates on DOM to get data)
                    parent = driver.find_element_by_xpath("//*[@id='content']/div[5]/div[" + str(div) + "]//strong[contains(text(),'" + field + "')]/parent::node()")
                    child = driver.find_element_by_xpath("//*[@id='content']/div[5]/div[" + str(div) + "]//strong[contains(text(),'" + field + "')]")
                    # Removing specific text of parent element from data
                    df_decision_column.append(parent.text.replace(child.text, ''))
                except:
                    # If the parent element of data does not exists, it includes Not Applicable in the list
                    df_decision_column.append('n/a')

            # saving columns on data frame
            df_decision.append(df_decision_column)

        # Closing WebDriver
        driver.quit()

        # Formatting dataframe
        df_decision_final = pd.DataFrame(df_decision).transpose()
        df_decision_final.columns = fields

        # Saving DataFrame as CSV
        df_decision_final.to_csv('tax-decision.csv',encoding='utf-8-sig')

if __name__ == '__main__':
    Main().run()
