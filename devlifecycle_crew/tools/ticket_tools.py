"""
Ticket management tools for the DevLifecycle Crew.
"""

from typing import Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class TicketInput(BaseModel):
    """Input schema for ticket operations."""
    title: str = Field(description="Title of the ticket")
    description: str = Field(description="Detailed description of the ticket")
    ticket_type: str = Field(
        default="task",
        description="Type of ticket: bug, feature, task, story, epic"
    )
    priority: str = Field(
        default="medium",
        description="Priority level: critical, high, medium, low"
    )
    labels: str = Field(
        default="",
        description="Comma-separated labels for the ticket"
    )


class TicketSearchInput(BaseModel):
    """Input schema for ticket search."""
    query: str = Field(description="Search query for finding tickets")
    status: str = Field(
        default="all",
        description="Filter by status: open, in_progress, closed, all"
    )
    limit: int = Field(default=10, description="Maximum number of results")


class TicketUpdateInput(BaseModel):
    """Input schema for ticket updates."""
    ticket_id: str = Field(description="ID of the ticket to update")
    field: str = Field(description="Field to update: status, priority, assignee, labels")
    value: str = Field(description="New value for the field")


class TicketCreatorTool(BaseTool):
    """Tool for creating tickets in the system."""
    
    name: str = "ticket_creator"
    description: str = (
        "Creates a new ticket in the ticket management system. "
        "Use this to create bugs, features, tasks, stories, or epics. "
        "Provide title, description, type, priority, and optional labels."
    )
    args_schema: Type[BaseModel] = TicketInput
    
    def _run(
        self,
        title: str,
        description: str,
        ticket_type: str = "task",
        priority: str = "medium",
        labels: str = ""
    ) -> str:
        """Create a ticket."""
        # In a real implementation, this would integrate with Jira, GitHub Issues, etc.
        import uuid
        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        
        label_list = [l.strip() for l in labels.split(",") if l.strip()]
        
        result = {
            "success": True,
            "ticket_id": ticket_id,
            "title": title,
            "type": ticket_type,
            "priority": priority,
            "labels": label_list,
            "status": "open",
            "message": f"Successfully created {ticket_type} ticket: {ticket_id}"
        }
        
        return str(result)


class TicketSearchTool(BaseTool):
    """Tool for searching tickets."""
    
    name: str = "ticket_search"
    description: str = (
        "Searches for existing tickets in the system. "
        "Use this to find related tickets, check for duplicates, "
        "or retrieve ticket information. Supports filtering by status."
    )
    args_schema: Type[BaseModel] = TicketSearchInput
    
    def _run(
        self,
        query: str,
        status: str = "all",
        limit: int = 10
    ) -> str:
        """Search for tickets."""
        # In a real implementation, this would search actual ticket systems
        # This is a mock implementation
        mock_results = [
            {
                "ticket_id": "TICKET-001",
                "title": f"Sample ticket matching: {query}",
                "status": "open",
                "priority": "medium",
                "type": "task"
            },
            {
                "ticket_id": "TICKET-002",
                "title": f"Related to: {query}",
                "status": "in_progress",
                "priority": "high",
                "type": "feature"
            }
        ]
        
        result = {
            "success": True,
            "query": query,
            "status_filter": status,
            "results_count": len(mock_results),
            "tickets": mock_results[:limit]
        }
        
        return str(result)


class TicketUpdaterTool(BaseTool):
    """Tool for updating ticket fields."""
    
    name: str = "ticket_updater"
    description: str = (
        "Updates a specific field of an existing ticket. "
        "Can update status, priority, assignee, or labels. "
        "Requires the ticket ID and the field/value to update."
    )
    args_schema: Type[BaseModel] = TicketUpdateInput
    
    def _run(
        self,
        ticket_id: str,
        field: str,
        value: str
    ) -> str:
        """Update a ticket field."""
        # In a real implementation, this would update actual ticket systems
        valid_fields = ["status", "priority", "assignee", "labels", "description"]
        
        if field.lower() not in valid_fields:
            return str({
                "success": False,
                "error": f"Invalid field '{field}'. Valid fields: {valid_fields}"
            })
        
        result = {
            "success": True,
            "ticket_id": ticket_id,
            "field_updated": field,
            "new_value": value,
            "message": f"Successfully updated {field} to '{value}' for ticket {ticket_id}"
        }
        
        return str(result)
