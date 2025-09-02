"""Dispatcher - Routes intents to appropriate handlers"""
from typing import Optional, Dict, Any
from core.policy.reply_style_enhanced import explain_cannot_with_fix, success_with_details

class Dispatcher:
    """Intent to action router"""
    
    def __init__(self):
        self.tools = {}
        self.load_tools()
    
    def load_tools(self):
        """Load available tools"""
        try:
            from core.tools.file_ops import FileOperations
            from core.tools.excel_pro import ExcelProcessor
            self.tools['file_ops'] = FileOperations()
            self.tools['excel'] = ExcelProcessor()
        except Exception as e:
            print(f"Tool loading error: {e}")
    
    async def try_local_tools(self, intent: Dict, message: str) -> Optional[str]:
        """Try to handle with local tools first"""
        intent_type = intent.get("intent", "")
        
        # File operations
        if "file" in intent_type or "dosya" in intent_type:
            if "list" in intent_type:
                return await self.tools['file_ops'].list_files()
            elif "open" in intent_type:
                return await self.tools['file_ops'].open_latest_image()
        
        # Excel operations
        elif "excel" in intent_type:
            return await self.tools['excel'].create_excel({})
        
        # Image operations
        elif "image.open" in intent_type:
            return await self.tools['file_ops'].open_latest_image()
        
        return None
    
    async def dispatch(self, intent: Dict, text: str) -> str:
        """Main dispatch logic"""
        # First try local tools
        result = await self.try_local_tools(intent, text)
        if result:
            return result
        
        # If no local tool, return None (orchestrator will try agents)
        return None
