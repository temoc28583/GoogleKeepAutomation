from bs4 import BeautifulSoup

class Notefetch:
    def __init__(self, notion_client, database_id):
        self.notion_client = notion_client
        self.database_id = database_id

    def get_all_notes(self):
        all_notes = {}
        start_cursor = None

        try:
            while True:
                query_params = {"database_id": self.database_id, "page_size": 100}
                if start_cursor:
                    query_params["start_cursor"] = start_cursor

                response = self.notion_client.databases.query(**query_params)

                for page in response["results"]:
                    page_id = page["id"]
                    title_property = page["properties"]["Name"]["title"]
                    if not title_property:
                        continue

                    title = title_property[0]["text"]["content"]
                    content = self._fetch_blocks_recursive(page_id)
                    all_notes[title] = {"id": page_id, "content": "\n".join(content)}

                if response.get("has_more"):
                    start_cursor = response["next_cursor"]
                else:
                    break

            return all_notes
        except Exception as e:
            print(f"Failed to fetch notes and content: {e}")
            return {}

    def get_all_pages_in_database(self):
        """Fetch all pages, including archived."""
        all_pages = []
        start_cursor = None

        try:
            while True:
                query_params = {"database_id": self.database_id, "page_size": 100}
                if start_cursor:
                    query_params["start_cursor"] = start_cursor

                response = self.notion_client.databases.query(**query_params)
                all_pages.extend(response["results"])

                if response.get("has_more"):
                    start_cursor = response["next_cursor"]
                else:
                    break

            return all_pages
        except Exception as e:
            print(f"Failed to fetch all pages: {e}")
            return []

    def _fetch_blocks_recursive(self, block_id):
        content = []
        try:
            blocks = self.notion_client.blocks.children.list(block_id=block_id)
            for block in blocks["results"]:
                block_type = block["type"]

                # Supported block types
                mapping = {
                    "paragraph": "paragraph",
                    "heading_1": "heading_1",
                    "heading_2": "heading_2",
                    "heading_3": "heading_3",
                    "bulleted_list_item": "bulleted_list_item",
                    "numbered_list_item": "numbered_list_item",
                    "quote": "quote",
                    "to_do": "to_do",
                    "callout": "callout"
                }

                if block_type in mapping:
                    rich_texts = block[block_type]["rich_text"]
                    for rt in rich_texts:
                        content.append(self.clean_html(rt["text"]["content"]))
                else:
                    print(f"Unsupported block type: {block_type}")

                if block.get("has_children"):
                    child_content = self._fetch_blocks_recursive(block["id"])
                    content.extend(child_content)

        except Exception as e:
            print(f"Error fetching blocks for block_id {block_id}: {e}")

        return content

    def clean_html(self, raw_html):
        return BeautifulSoup(raw_html, "html.parser").get_text()

    def del_notes(self, page_id):
        try:
            self.notion_client.pages.update(page_id=page_id, archived=True)
            print(f"Archived note {page_id} successfully.")
            return True
        except Exception as e:
            print(f"Error archiving note {page_id}: {e}")
            return False

    def unarchive_note(self, page_id):
        try:
            self.notion_client.pages.update(page_id=page_id, archived=False)
            print(f"Unarchived note {page_id} successfully.")
            return True
        except Exception as e:
            print(f"Error unarchiving note {page_id}: {e}")
            return False
