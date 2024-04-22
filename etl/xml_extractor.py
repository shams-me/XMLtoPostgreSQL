import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Generator, List

from lxml import etree
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class XMLExtractor:
    def __init__(self, path_to_xml: str | Path, chunk_size: int = 100) -> None:
        """
        Initialize the XMLExtractor with the path to the XML file and the chunk size for data extraction.

        Args:
            path_to_xml (str): A path to the XML file containing the data to be extracted.
            chunk_size (int): The size of the data chunks to be extracted from the XML file.
        Return: None
        """
        self.path_to_xml = Path(path_to_xml)
        self.chunk_size = chunk_size

    def extract_categories(self, main_tag: str = "categories", tag: str = "category") -> dict:
        """
        Extract categories from the XML file and return them as a dictionary.

        Args:
            main_tag (str): The XML tag containing categories.
            tag (str): The XML tag for categories.

        Returns:
            dict: A dictionary containing categories with their IDs, parent IDs, and text.
        """
        categories = {}
        context = etree.iterparse(self.path_to_xml, tag=main_tag, events=("end",))

        for _, elements in context:
            for element in elements.iter():
                if element.tag == tag:
                    cat_id = int(element.get("id"))
                    parent_id = int(element.get("parentId")) if element.get("parentId") else None
                    text = element.text
                    categories[cat_id] = {"parent_id": parent_id, "text": text}
            elements.clear()
            if elements.tag == main_tag:
                break

        del context
        return categories

    def extract(
        self,
        model: type[BaseModel],
        tag: str,
        category_main_tag: str,
        category_tag: str,
    ) -> Generator[List[type[BaseModel]], None, None]:
        """
        Load categories from the XML file.

        Args:
            model (type[BaseModel]): The Pydantic model to be loaded.
            tag (str): The XML tag to be loaded.
            category_main_tag (str): The XML tag for the main category.
            category_tag (str): The XML tag for categories.

        Yields:
            Generator[List[type[BaseModel]], None, None]: A generator that yields batches of categories.
        """
        categories = self.extract_categories(main_tag=category_main_tag, tag=category_tag)
        batch = []
        context = etree.iterparse(self.path_to_xml, tag=tag, events=("end",))
        for _, element in context:
            obj = self._parse_element(element, model, categories)
            element.clear()
            batch.append(obj)
            if self.chunk_size and len(batch) >= self.chunk_size:
                yield batch
                batch = []
        del context

        if batch:
            yield batch

    def _parse_element(self, element: etree.Element, model: type[BaseModel], categories: dict) -> BaseModel:
        """
        Parse a single XML element into a Pydantic model object.

        Args:
            element (etree.Element): The XML element to be parsed.
            model (type[BaseModel]): The Pydantic model to parse the element into.

        Returns:
            BaseModel: The parsed Pydantic model object.
        """

        features = {param.get("name"): param.text for param in element.findall("param")}
        _recursive_categories = self._recursive_category(int(element.find("categoryId").text), categories)
        obj = model(
            uuid=uuid.uuid4(),
            product_id=int(element.get("id")),
            title=element.find("name").text,
            description=element.find("description").text if element.find("description") else None,
            seller_name=element.find("vendor").text if element.find("vendor") else None,
            first_image_url=element.find("picture").text,
            category_id=int(element.find("categoryId").text),
            category_lvl_1=_recursive_categories.pop(0) if _recursive_categories else None,
            category_lvl_2=_recursive_categories.pop(0) if _recursive_categories else None,
            category_lvl_3=_recursive_categories.pop(0) if _recursive_categories else None,
            categories_remaining="/".join(_recursive_categories) if _recursive_categories else None,
            features=json.dumps(features),
            inserted_at=datetime.fromtimestamp(int(element.find("modified_time").text)),
            updated_at=datetime.fromtimestamp(int(element.find("modified_time").text)),
            currency=element.find("currencyId").text,
            barcode=int(element.find("barcode").text) if element.find("barcode") else None,
        )
        return obj

    def _recursive_category(self, category_id: int, categories: dict) -> List[str]:
        """
        Recursively get the path to the category from the root category.

        Args:
            category_id (int): The ID of the category.
            categories (dict): A dictionary of categories with their parent IDs.
        Returns:
            List[str]: A list of category names from the root category to the given category.
        """
        if category_id not in categories:
            return []
        category = categories[category_id]
        return self._recursive_category(category["parent_id"], categories) + [category["text"]]
