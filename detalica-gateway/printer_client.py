import win32print
import win32ui
import requests
import time

API_URL = "http://localhost:3000"
CLIENT_ID = "client123"
PRINTER_NAME = "POS-80"
MAX_WIDTH = 600  # Adjust based on your printer's width in pixels (for 80mm paper)

def check_printer_connection():
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
        printer_names = [p[2] for p in printers]
        if PRINTER_NAME in printer_names:
            print(f"Printer found: {PRINTER_NAME}")
            return True
        else:
            print(f"Printer not found. Available printers: {printer_names}")
            return False
    except Exception as e:
        print(f"Printer connection error: {e}")
        return False

def wrap_text(hdc, text, max_width):
    """Wrap text to fit within the specified width using hdc.GetTextExtent."""
    wrapped_text = []
    words = text.split(' ')
    line = ''
    
    for word in words:
        # Check if the word fits in the line
        if hdc.GetTextExtent(line + ' ' + word)[0] <= max_width:
            line += ' ' + word
        else:
            wrapped_text.append(line)
            line = word
    
    if line:
        wrapped_text.append(line)
    
    return wrapped_text

def test_print():
    try:
        # Open printer
        hprinter = win32print.OpenPrinter(PRINTER_NAME)
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(PRINTER_NAME)
        hdc.StartDoc("Test Print")
        hdc.StartPage()

        # Create font for text
        font = win32ui.CreateFont({
            "name": "Arial",
            "height": 25,  # Adjust the height (font size)
            "weight": 500,
        })
        hdc.SelectObject(font)

        # Simple text output
        hdc.TextOut(10, 10, "POS-80 Test Print")
        hdc.TextOut(10, 30, "=" * 20)
        hdc.TextOut(10, 50, f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        hdc.TextOut(10, 70, "Width: 80mm")

        hdc.EndPage()
        hdc.EndDoc()
        win32print.ClosePrinter(hprinter)
        print("Test print sent to POS-80.")
    except Exception as e:
        print(f"Test print error: {e}")

def check_commands():
    try:
        response = requests.get(f"{API_URL}/commands/{CLIENT_ID}", timeout=5)
        data = response.json()
        content = data.get("content", "")

        if content:
            if content.startswith("DLL:"):
                print("Government .dll placeholder - awaiting function details")
            else:
                hprinter = win32print.OpenPrinter(PRINTER_NAME)
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(PRINTER_NAME)
                hdc.StartDoc("Print Job")
                hdc.StartPage()

                # Create font for text
                font = win32ui.CreateFont({
                    "name": "Arial",
                    "height": 25,  # Adjust font size
                    "weight": 500,
                })
                hdc.SelectObject(font)

                # Split the content into lines at each newline character
                lines = content.splitlines()
                y_position = 10
                for line in lines:
                    # Wrap the line to fit within the max width
                    wrapped_text = wrap_text(hdc, line, MAX_WIDTH)
                    for wrapped_line in wrapped_text:
                        hdc.TextOut(10, y_position, wrapped_line)
                        y_position += 30  # Adjust line spacing

                hdc.EndPage()
                hdc.EndDoc()
                win32print.ClosePrinter(hprinter)
                print(f"Printed: {content}")
    except Exception as e:
        print(f"Error fetching commands: {e}")

def main():
    print("Thermal Printer Client starting for POS-80...")

    if not check_printer_connection():
        print("POS-80 not found. Check printer name and connection.")
        return

    test_print()

    while True:
        check_commands()
        time.sleep(2)  # Poll every 2 seconds

if __name__ == "__main__":
    main()
