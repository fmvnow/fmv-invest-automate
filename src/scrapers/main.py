import os
import pdfplumber
import csv
import re

def get_stocks_from_text(text):
    stocks = []
    for line in text.splitlines():
        if "1-BOVESPA" in line:
            parts = line.split()
            acoes = re.sub(r"^1-BOVESPA C (VISTA|FRACIONARIO)", "", line)
            acoes = re.sub(r"(\sN2|\sNM|\sCI|\sN1).*", "", acoes).strip()
            
            trade = {
                "acoes": acoes,
                "qtde": parts[-4],
                "preco-medio": parts[-3],
                "formula-preco-medio": f"({parts[-3]} * {parts[-4]})"
            }
            
            stocks.append(trade)
    
    if not stocks:
        print("Nenhum dado encontrado.")
        return
        
    return stocks

def extract_stocks_from_pdf(pdf_path):
    """
    Reads the PDF file and extracts trade information.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            stocks = []
            
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    stocks.append(get_stocks_from_text(text))
                    if not stocks:
                        print(f"Nenhum dado encontrado na página {page_number} do arquivo {pdf_path}.")
                        continue
                else:
                    print("Nenhum texto encontrado nesta página.")
            
            return stocks


    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")

def save_stocks_to_csv(stocks):
    """
    Saves the stock data to a CSV file in the ./src/csv directory.
    """
    # Create the ./src/csv directory if it doesn't exist
    csv_directory = "./src/csv"
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    # Path to the CSV file
    csv_file_path = os.path.join(csv_directory, "stocks.csv")

    # Save the data to a CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(["Ações", "Quantidade", "Fórmula Preço Médio"])

        # Write the data
        for trade in stocks:
            writer.writerow([trade['acoes'], trade['qtde'], trade['formula-preco-medio']])

    print(f"Os dados foram salvos no arquivo {csv_file_path}.")

def save_stocks_to_md(stocks):
    """
    Saves the stock data to a Markdown (.md) file in the ./src/md directory.
    """
    # Create the ./src/md directory if it doesn't exist
    md_directory = "./src/md"
    if not os.path.exists(md_directory):
        os.makedirs(md_directory)

    # Path to the Markdown file
    md_file_path = os.path.join(md_directory, "stocks.md")

    # Save the data to a Markdown file
    with open(md_file_path, mode='w', encoding='utf-8') as md_file:
        # Write the data
        for trade in stocks:
            md_file.write(f"## {trade['acoes']}\n")
            md_file.write(f"Quantidade: {trade['qtde']}\n")
            md_file.write(f"Fórmula preço médio: {trade['formula-preco-medio']}\n")
            md_file.write("--------\n\n")

    print(f"Os dados foram salvos no arquivo {md_file_path}.")

def print_stocks(stocks):
        """
        Prints the stock data to the console.
        """
        for trade in stocks:
            print(f"Trade: {trade['acoes']}")
            print(f"Quantidade: {trade['qtde']}")
            print(f"Fórmula preço médio: {trade['formula-preco-medio']}")
            print("-----")

def group_stocks(stocks): 
    grouped_stocks = {}
    for trade in stocks:
        acoes = trade['acoes']
        if acoes not in grouped_stocks:
            grouped_stocks[acoes] = {
                "acoes": acoes,
                "qtde": trade['qtde'],
                "formula-preco-medio": trade['formula-preco-medio']
            }
        else:
            grouped_stocks[acoes]["qtde"] += f" + {trade['qtde']}"
            grouped_stocks[acoes]["formula-preco-medio"] += f" + {trade['formula-preco-medio']}"
    return list(grouped_stocks.values())

def main():
    """
    Main function to process all PDFs in the /notas directory.
    """
    pdf_directory = "./src/notas"
    if not os.path.exists(pdf_directory):
        print(f"A pasta {pdf_directory} não existe.")
        return

    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    if not pdf_files:
        print("Nenhum arquivo PDF encontrado na pasta /notas.")
        return
    stocks = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        extracted_stocks = extract_stocks_from_pdf(pdf_path)
        if extracted_stocks:
            for stock_list in extracted_stocks:
                if stock_list:
                    stocks.extend(stock_list)

    stocks = group_stocks(stocks)
    print('stocks', stocks)
    

    # save_stocks_to_csv(stocks)
    save_stocks_to_md(stocks)
    print_stocks(stocks)

if __name__ == "__main__":
    main()