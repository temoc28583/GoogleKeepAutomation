from bs4 import BeautifulSoup

class Notefetch:
    def __init__(self, notion_client, database_id):
        self.notion_client = notion_client
        self.database_id = database_id

    def get_all_notes(self):
        try:
            response = self.notion_client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Platform",
                    "select": {
                        "equals": "Google Keep"
                    }
                }
            ) #creates a response object that queries the database to find the notes from Google Keep by calling the notion API

            all_notes = {}
            for page in response["results"]:#represents each page in the Notion Database, a page is a container for content with headers, paraggraph(a record of each note)
                page_id = page["id"] #retrieves page id within the page or a container for content with headers,pargraphs as blocks(unique identifier for the page)
                title_property = page["properties"]["Name"]["title"] #retrieves the Name property from the page(title is a property from database and is contained Name) from metdata column properties
                if not title_property:
                    continue
#examples of blocks are headings, paragraphs, bulleted lists,etc within a page. Children blocks are blocks that contain other blocks within blocks(nested blocks)
                title = title_property[0]["text"]["content"] #takes the first segment[0] of the title property
                content = self._fetch_blocks_recursive(page_id) #used in case of nested blocks within the page and also to get the content
                all_notes[title] = "\n".join(content) #stores the content of the notes in a dictionary with the title

            return all_notes

        except Exception as e:
            print(f"Failed to fetch notes and content: {e}")
            return {}

    def _fetch_blocks_recursive(self, block_id):
        content = [] #used to collect cleaned text content from the blocks

        try:
            blocks = self.notion_client.blocks.children.list(block_id=block_id) #each block can be a paragraph, header, bullet but ultitemly takes the API to extract content within the block

            for block in blocks["results"]: #loops through each block 
                block_type = block["type"] #checks type of the block
                rich_texts = [] #list of content objects within the block

                if block_type == "paragraph":
                    rich_texts = block["paragraph"]["rich_text"] #pulls out the content(rich text) from the paragraph block
                elif block_type == "heading_1":
                    rich_texts = block["heading_1"]["rich_text"] #pulls out the content(rich text) from the heading_1 block
                elif block_type == "heading_2":
                    rich_texts = block["heading_2"]["rich_text"]# pulls out the content(rich text) from the heading_2 block
                elif block_type == "heading_3":# pulls out the content(rich text) from the heading_3 block
                    rich_texts = block["heading_3"]["rich_text"]# pulls out the content(rich text) from the heading_3 block
                elif block_type == "bulleted_list_item":
                    rich_texts = block["bulleted_list_item"]["rich_text"]# pulls out the content(rich text) from the bulleted_list_item block
                elif block_type == "numbered_list_item":
                    rich_texts = block["numbered_list_item"]["rich_text"] # pulls out the content(rich text) from the numbered_list_item block
                elif block_type == "quote":# pulls out the content(rich text) from the quote block
                    rich_texts = block["quote"]["rich_text"]
                else:
                    print(f"Unsupported block type: {block_type}")
                # Clean and append rich text content(which is rt in its formatted form of content within one block)
                for rt in rich_texts: #loops through rich text segments(represented as a dict) within the block ecspecially if there are multiple(ex, Hello World! is a seperate rt object)
                    content.append(self.clean_html(rt["text"]["content"])) #strips html tags and appends the cleaned text fo content
                # We use rt["text"]["content"] to get the rich text that may be formatted uniquely to make it clean
                if block.get("has_children"):
                    child_content = self._fetch_blocks_recursive(block["id"]) #fetches child blocks content recurively if the notes are nested with multiple blocks within one block
                    content.extend(child_content) #adds on the child content to the main content list

        except Exception as e:
            print(f"Error fetching blocks for block_id {block_id}: {e}")

        return content


    def clean_html(self, raw_html):
        soup = BeautifulSoup(raw_html, "html.parser") #removes html attributes from the html content within the notes
        return soup.get_text()
