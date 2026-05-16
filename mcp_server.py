import logging
import os
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(_log_dir, exist_ok=True)
_handler = logging.FileHandler(os.path.join(_log_dir, "mcp_server.log"))
_handler.setLevel(logging.DEBUG)
_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"))
logging.getLogger().addHandler(_handler)
logging.getLogger().setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

mcp = FastMCP("DocumentMCP", log_level="WARNING")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string."
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        logger.warning("read_doc_contents: doc not found — %s", doc_id)
        raise ValueError(f"Doc with id {doc_id} not found")
    logger.info("read_doc_contents: %s", doc_id)
    return docs[doc_id]


@mcp.tool(
    name="read_bonbon_data",
    description="Read bonbon data and return it as a string when user requests it."
)
def read_bonbon_data():
    return "Sample bonbon data. BonBon is really just Xaltura"

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    if doc_id not in docs:
        logger.warning("edit_document: doc not found — %s", doc_id)
        raise ValueError(f"Doc with id {doc_id} not found")
    logger.info(
        "edit_document: %s | '%.60s%s' → '%.60s%s'",
        doc_id,
        old_str, "..." if len(old_str) > 60 else "",
        new_str, "..." if len(new_str) > 60 else "",
    )
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
        Your goal is to reformat a document to be written with markdown syntax.

        The id of the document you need to reformat is:
        <document_id>
        {doc_id}
        </document_id>

        Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
        Use the 'edit_document' tool to edit the document. After the document has been reformatted...
        """
    return [ base.UserMessage(prompt)]
# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
