"""
Макросы для MkDocs документации Calendar API
"""

def define_env(env):
    """
    Определяет переменные и функции для использования в документации.
    """
    
    # Глобальные переменные
    env.variables['api_base_url'] = 'http://localhost:8000/api'
    env.variables['project_name'] = 'Calendar API'
    env.variables['version'] = '0.1.0'
    
    # Ваши кастомные переменные
    env.variables['dssd'] = 'Ваше значение для dssd'
    env.variables['server_port'] = 8000
    env.variables['docs_port'] = 8001
    
    # Типы событий
    env.variables['event_types'] = {
        0: 'Default',
        1: 'Meetings/Planning', 
        2: 'Development/Technical',
        3: 'Demo/Presentations',
        4: 'Informal Events'
    }
    
    @env.macro
    def curl_example(endpoint, method='GET', params=None, body=None):
        """
        Генерирует пример curl команды.
        """
        base_url = env.variables['api_base_url']
        url = f"{base_url}{endpoint}"
        
        if params:
            param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
            url += f"?{param_str}"
        
        cmd = f"curl -X '{method}' \\\n  '{url}'"
        
        if method in ['POST', 'PUT', 'PATCH'] and body:
            cmd += " \\\n  -H 'Content-Type: application/json'"
            if isinstance(body, dict):
                import json
                body_str = json.dumps(body, indent=2, ensure_ascii=False)
                cmd += f" \\\n  -d '{body_str}'"
            else:
                cmd += f" \\\n  -d '{body}'"
        
        return f"```bash\n{cmd}\n```"
    
    @env.macro
    def api_endpoint(method, path, description=""):
        """
        Генерирует заголовок для API endpoint с эмодзи.
        """
        method_emoji = {
            'GET': '🟢',
            'POST': '🔴', 
            'PUT': '🟡',
            'PATCH': '🟣',
            'DELETE': '⚫'
        }
        
        emoji = method_emoji.get(method.upper(), '⚪')
        return f"# {emoji} {method.upper()} {path}\n\n{description}"
    
    @env.macro
    def event_type_table():
        """
        Генерирует таблицу типов событий.
        """
        types = env.variables['event_types']
        
        table = "| Код | Тип события |\n"
        table += "|-----|-------------|\n"
        
        for code, name in types.items():
            table += f"| `{code}` | {name} |\n"
        
        return table
    
    @env.macro
    def response_example(data, status_code=200):
        """
        Генерирует пример ответа API.
        """
        import json
        
        if isinstance(data, (dict, list)):
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            json_str = str(data)
        
        return f"**Статус:** `{status_code}`\n\n```json\n{json_str}\n```"
    
    @env.macro
    def parameter_description(name, type_name, description, required=False, default=None):
        """
        Генерирует описание параметра.
        """
        req_text = "**обязательный**" if required else "необязательный"
        default_text = f", по умолчанию: `{default}`" if default is not None else ""
        
        return f"- **{name}** `[{type_name}]`: {description} ({req_text}{default_text})"
