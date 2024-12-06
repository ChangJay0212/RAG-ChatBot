import os
from typing import Any, Dict, List, Optional

import pymupdf
from jinja2 import Template
from llama_index.core import Document
from llama_index.core.readers.base import BaseReader
from pymupdf import Document as FitzDocument

from core.models import Llama31Model


class AI_PDFLoader(BaseReader):
    def __init__(
        self,
        *args: Any,
        prompt: dict = {
            "system": """
You will receive a Messy Information. Please process them step-by-step using Chain-of-Thought reasoning and convert them into Markdown format. Categorize the data and format it accordingly without mentioning any "steps" in the final output. The final output should only include the converted Markdown data, structured into sections like "Contact Information," "Specifications," and "Order Information."

Follow these guidelines:
    1. Identify the contact details and format them as a Markdown list under "Contact Information."
    2. Organize the product specifications into a Markdown table under "Specifications."
    3. List the product's key features as bullet points under "Features."
    4. Provide the order information, including the model number and description, under "Order Information."

Ensure that the output is clean and well-structured in Markdown, without any references to steps or the process followed.

Example Output:

1. Step 1: Organize the Contact Information
    - This section contains the headquarters and branch office contact details, which I will format into lists.
    - The headquarters is located in Taiwan, followed by contact details for four different regional offices.

    The Markdown list format is:
    ```markdown
    ## Contact Information
    - **Headquarters (Taiwan):**
      - Address: 5F., No. 237, Sec. 1, Datong Rd., Xizhi Dist., New Taipei City 221, Taiwan
      - Phone: +886-2-77033000
      - Email: [sales@innodisk.com](mailto:sales@innodisk.com)

    ### Branch Offices:
    - **USA:** usasales@innodisk.com, +1-510-770-9421
    - **Europe:** eusales@innodisk.com, +31-40-3045-400
    - **Japan:** jpsales@innodisk.com, +81-3-6667-0161
    - **China:** sales_cn@innodisk.com, +86-755-21673689
    ```

2. Step 2: Organize the Product Specifications
    - Here, I will extract and organize all technical specifications and place them in a table. A table helps clearly present technical data for easier comparison and understanding.
    - For example, the technical specifications table is:

    ```markdown
    ## Specifications

    | **Feature**                 | **Details**                                 |
    |-----------------------------|---------------------------------------------|
    | **Form Factor**              | M.2 3042-B-M                                |
    | **Input Interface**          | PCI Express 2.0                             |
    | **Output Interface**         | SATA III                                    |
    | **Output Connector**         | SATA 7pin x 4                               |
    | **Bridge Chip**              | Marvell 88SE9215                            |
    | **TDP**                      | 2.74W (3.3V x 830mA)                        |
    | **Dimensions**               | 30 x 42 x 13.8 mm                           |
    | **Weight**                   | 7.5g                                        |
    | **Temperature Range**        | Operation: 0°C ~ +70°C                      |
    |                             | Storage: -55°C ~ +95°C                      |
    | **Environmental Resistance** | Vibration: 5G @ 7~2000Hz                    |
    |                             | Shock: 50G @ 0.5ms                          |
    ```

3. Step 3: List Product Features
    - Next, I will list the product features, which are usually the highlights or unique aspects of the product. These will be presented as bullet points.

    ```markdown
    ## Features
    - M.2 3042 to four SATA III Module.
    - PCI Express 2.0 to four SATA III ports.
    - Supports AHCI, Port Multiplier.
    - Supports Native Command Queuing.
    - Supports error reporting, recovery, and correction.
    - 30µ golden finger.
    - Industrial design, manufactured in Taiwan by Innodisk.
    - 3-year warranty.
    ```

4. Step 4: Order Information
    - Finally, I will provide the order information, including the model number and product description.

    ```markdown
    ## Order Information
    - **Model Number:** EGPS-3401-C1
    - **Description:** M.2 to four SATA III Module, SATAIII 7pin Male
    ```
---

This Chain-of-Thought approach will show each step of the thought process, guiding the model to gradually organize and format the data. Each step explains how the raw data is extracted and converted into Markdown, especially for handling complex or structured technical information.
""",
            "user": """
    Messy Information:
    {{ messy_info }}
""",
            "test": """
    The following Messy Information of product specification document already contains the product name. Please identify and return the product name as it appears in the document.
""",
        },
        model: Llama31Model,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.prompt = prompt
        self.model = model

    def load_data(
        self, pdf_path_or_url: str, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Load data and extract table from PDF file.

        Args:
            pdf_path_or_url (str): A url or file path pointing to the PDF

        Returns:
            List[Document]: List of documents.
        """
        results = []
        # Check if the file exists
        if not os.path.exists(pdf_path_or_url):
            raise FileNotFoundError(f"The PDF path {pdf_path_or_url} does not exist.")

        doc: FitzDocument = pymupdf.open(pdf_path_or_url)
        for page_number in range(doc.page_count):
            page = doc.load_page(page_number)
            text = page.get_text()
            template = Template(self.prompt["user"])

            # print(f"Page {page_number + 1}:\n{text}\n")
            final_prompt = template.render(messy_info=text)

            prompt = [
                {"role": "system", "content": self.prompt["system"]},
                {"role": "user", "content": final_prompt},
            ]
            markdown_output = ""

            for data in self.model.run(prompt=prompt, max_tokens=5000):
                if isinstance(data, str):
                    markdown_output += data  # Assume result is a full string

            doc_info = {
                "page_number": page_number + 1,  # page numbers start at 1
                "pdf_path": str(pdf_path_or_url),
                **(extra_info or {}),  # Add any extra info passed in
            }
            document = Document(text=markdown_output, extra_info=doc_info)

            results.append(document)
        doc.close()
        return results


if __name__ == "__main__":
    pass
