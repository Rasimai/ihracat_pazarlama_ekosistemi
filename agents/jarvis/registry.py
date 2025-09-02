"""Plugin Discovery & Skill Registry System"""
import yaml
import importlib
from pathlib import Path
from typing import Dict, List, Optional

class SkillRegistry:
    """Alt asistanları ve yeteneklerini yöneten merkezi kayıt sistemi"""
    
    def __init__(self):
        self.skills: Dict[str, List[str]] = {}
        self.agents: Dict[str, object] = {}
        self.skill_to_agent: Dict[str, str] = {}
        self.discover_agents()
    
    def discover_agents(self):
        """Tüm agent klasörlerini tara ve yükle"""
        agents_dir = Path(__file__).parent.parent
        
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir() and agent_dir.name not in ["__pycache__", "jarvis"]:
                skills_file = agent_dir / "skills.yaml"
                agent_file = agent_dir / "agent.py"
                
                if skills_file.exists() and agent_file.exists():
                    self.load_agent(agent_dir.name, skills_file, agent_file)
    
    def load_agent(self, agent_name: str, skills_file: Path, agent_file: Path):
        """Bir agent'ı ve yeteneklerini yükle"""
        try:
            # Skills yükle
            with open(skills_file) as f:
                config = yaml.safe_load(f)
                self.skills[agent_name] = config.get("skills", [])
                
                # Skill-to-agent mapping
                for skill in config.get("skills", []):
                    self.skill_to_agent[skill] = agent_name
            
            # Agent class'ını yükle
            module_name = f"agents.{agent_name}.agent"
            module = importlib.import_module(module_name)
            agent_class = getattr(module, f"{agent_name.upper()}Agent")
            self.agents[agent_name] = agent_class()
            
            print(f"✓ Loaded {agent_name}: {len(self.skills[agent_name])} skills")
            
        except Exception as e:
            print(f"✗ Failed to load {agent_name}: {e}")
    
    def find_agent_for_skill(self, skill: str) -> Optional[str]:
        """Bir skill için uygun agent'ı bul"""
        # Exact match
        if skill in self.skill_to_agent:
            return self.skill_to_agent[skill]
        
        # Partial match
        for s, agent in self.skill_to_agent.items():
            if skill in s or s in skill:
                return agent
        
        return None
    
    def get_agent(self, agent_name: str) -> Optional[object]:
        """Agent instance'ını getir"""
        return self.agents.get(agent_name)
    
    def list_all_skills(self) -> Dict[str, List[str]]:
        """Tüm agent ve skill'leri listele"""
        return self.skills

# Global registry instance
registry = SkillRegistry()
