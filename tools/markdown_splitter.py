import os
import re

from llama_index.core.node_parser.relational.base_element import BaseElementNodeParser
from llama_index.core.schema import TextNode


class i:
    def __init__(self) -> None:
        pass


class MarkdownSplitterNodeParser:
    def __init__(self, separator="##", tagging: bool = True) -> None:
        self.separator = separator
        self.tagging = tagging

    def _extract_product_code(self, filepath: str) -> str:
        # print(filepath)
        filename = os.path.basename(filepath)
        # Regular expression to capture the product code in the path before _Datasheet.pdf
        # match = re.search(r'(?:Innodisk_)?([A-Za-z0-9_]+)_Datasheet\.pdf|Innodisk_([A-Za-z0-9_]+)_Technical_Product_Specification', filepath)
        # if match:
        #     # Return the non-empty group
        #     return match.group(1) if match.group(1) else match.group(2)
        # return None
        return filename

    def get_nodes_from_documents(self, docs: list) -> list:
        nodes = []

        for doc in docs:
            splits = re.split(r"(?=(?<!#)##(?!#))", doc.text)

            for split_text in splits:
                if split_text.strip() and split_text.strip().startswith(self.separator):
                    text = split_text.strip()
                    if self.tagging and doc.metadata["pdf_path"]:
                        product_name = self._extract_product_code(
                            filepath=doc.metadata["pdf_path"]
                        )
                        # print(product_name)
                        if product_name:
                            text = f"{product_name}\n" + text
                    nodes.append(TextNode(text=text, metadata=doc.metadata))
        return nodes


if __name__ == "__main__":
    from llama_index.core import Document

    docs = []
    document = Document(
        text="""**'Let's process the messy information step by step using Chain-of-Thought reasoning.

    **Step 1: Categorize and format contact information**

    * The contact information is located at the end of the document, on page 19.
    * I will extract the contact details and format them as a Markdown list.

    ```
    ## Contact Information
    - **Contact Us:** Innodisk Corporation
    - Address: [insert address]
    - Phone: [insert phone number]
    - Email: [sales@innodisk.com](mailto:sales@innodisk.com)
    ```

    **Step 2: Organize product specifications**

    * I will extract and organize the technical specifications from sections 2.1 to 2.6.
    * A table format is suitable for presenting technical data.

    ```markdown
    ## Product Specifications

    | **Feature**                 | **Details**                                 |
    |-----------------------------|---------------------------------------------|
    | **Form Factor**              | [insert form factor]                         |
    | **Input Interface**          | PCI Express 2.0                             |
    | **Output Interface**         | SATA III                                    |
    | **Power Requirement**        | [insert power requirement]                  |
    | **Temperature Range**        | [insert temperature range]                  |
    | **Humidity**                 | [insert humidity]                           |
    | **Shock and Vibration**      | [insert shock and vibration]                |
    | **MTBF**                     | [insert MTBF]                               |
    | **CE and FCC Compatibility** | Compliant                                  |
    | **RoHS Compliance**           | Compliant                                  |
    ```

    Please provide the details for each feature, or I'll wait for your input.

    **Step 3: List product features**

    * Next, I will extract and list the product's key features from section 1.2.
    * These will be presented as bullet points.

    ```markdown
    ## Features
    - PCI Express 2.0 to four SATA III ports.
    - Supports AHCI, Port Multiplier.
    - Supports Native Command Queuing.
    ```

    **Step 4: Order information**

    * Finally, I will provide the order information, including the model number and description.

    Please note that the model number "EGPU-3201" is mentioned at the beginning of the document. I will also extract any relevant product description from the document.

    ```
    ## Order Information
    - **Model Number:** EGPU-3201
    - **Description:** [insert description]
                        """
    )
    docs.append(document)
    document_splitter = MarkdownSplitterNodeParser(tagging=False)
    nodes = document_splitter.get_nodes_from_documents(docs)

    for i, node in enumerate(nodes):
        print(node)
        print("*" * 20, "\n")
