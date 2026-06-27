import io
import PyPDF2
from typing import Union, BinaryIO

class PDFReaderError(Exception):
    """Base exception class for PDF reader errors."""
    pass

class EncryptedPDFError(PDFReaderError):
    """Raised when the PDF file is password protected/encrypted."""
    pass

class CorruptedPDFError(PDFReaderError):
    """Raised when the PDF file is corrupted and cannot be read."""
    pass

class EmptyPDFError(PDFReaderError):
    """Raised when the PDF file has no readable text content."""
    pass

def extract_text_from_pdf(pdf_file: Union[str, io.BytesIO, BinaryIO]) -> str:
    """
    Extracts plain text from a PDF file.
    Supports file paths, BytesIO streams, or file-like objects (e.g. from Streamlit).
    
    Args:
        pdf_file (Union[str, io.BytesIO, BinaryIO]): Path to the PDF file or a file-like stream object.
        
    Returns:
        str: The extracted text content.
        
    Raises:
        EncryptedPDFError: If the PDF is encrypted/password protected.
        CorruptedPDFError: If the PDF is corrupt.
        EmptyPDFError: If no text is found in the PDF.
        PDFReaderError: General failures.
    """
    try:
        # Determine if we need to open a file path or use the stream directly
        if isinstance(pdf_file, str):
            f = open(pdf_file, 'rb')
        else:
            f = pdf_file

        try:
            reader = PyPDF2.PdfReader(f)
            
            # Check for encryption
            if reader.is_encrypted:
                # Try decrypting with empty password
                try:
                    if reader.decrypt("") == 0:
                        raise EncryptedPDFError("The uploaded PDF is encrypted/password protected and cannot be read.")
                except Exception:
                    raise EncryptedPDFError("The uploaded PDF is encrypted/password protected and cannot be read.")
            
            # Extract text page by page
            extracted_text = []
            num_pages = len(reader.pages)
            
            if num_pages == 0:
                raise EmptyPDFError("The PDF contains no pages.")
                
            for page_num in range(num_pages):
                try:
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        extracted_text.append(text)
                except Exception as page_err:
                    # Ignore minor errors on individual pages and try other pages,
                    # unless it's the only page
                    if num_pages == 1:
                        raise CorruptedPDFError(f"Error reading page 1 of the PDF: {page_err}")
            
            combined_text = "\n".join(extracted_text).strip()
            
            if not combined_text:
                raise EmptyPDFError("No readable text was found in the PDF. It might be scanned or image-only. Please upload a text-based PDF.")
                
            return combined_text
            
        except PyPDF2.errors.DependencyError as dep_err:
            raise PDFReaderError(f"System library error while decoding PDF: {dep_err}")
        except PyPDF2.errors.PdfReadError as read_err:
            raise CorruptedPDFError(f"The PDF is corrupted or invalid: {read_err}")
        except Exception as e:
            if isinstance(e, PDFReaderError):
                raise e
            raise CorruptedPDFError(f"An unexpected error occurred while parsing the PDF: {str(e)}")
            
        finally:
            if isinstance(pdf_file, str):
                f.close()
                
    except FileNotFoundError:
        raise PDFReaderError("The specified PDF file path was not found.")
    except Exception as general_err:
        if isinstance(general_err, PDFReaderError):
            raise general_err
        raise PDFReaderError(f"Failed to open/process the PDF file: {str(general_err)}")
