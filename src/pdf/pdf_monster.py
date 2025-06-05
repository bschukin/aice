import inspect

from agents.baseagent import BaseAgent
from pdf.pdf_reader import read_pdf, read_docx


class PdfMonster(BaseAgent):

    def __init__(self, name: str = "PdfMonster", project: str = 'pdf'):
        super().__init__(role="pdf", name=name, project=project, prompt_dir="src.pdf.prompts")

    def _get_system_prompt(self) -> list[dict[str, str]]:
        agent_prompt = {'role': 'system', 'content': self._prompt.agent_prompt}
        return [agent_prompt]

    def get_result(self, cls, file_name):
        prompt = self._get_system_prompt()
        pyd_prompt = {'role': 'system', 'content': self.get_pydantic(cls)}
        user_prompt = {'role': 'user', 'content': 'Сформируй структуру для следующего текста из файла'}
        prompt.append(pyd_prompt)
        prompt.append(user_prompt)

        txt = read_pdf(self._project, file_name)
        text_prompt = {'role': 'user', 'content': f"Текст из файла: \n\n{txt}"}
        prompt.append(text_prompt)

        resp = self._gate().request(prompt)
        return resp

    def get_result_docx(self, file_name, *cls):
        prompt = self._get_system_prompt()
        pyd_prompt = {'role': 'system', 'content': self.get_pydantics(*cls)}
        resp_propmps = []
        prompt.append(pyd_prompt)

        txt = read_docx(self._project, file_name)
        chunks = self.split_into_chunks(txt, 100000)
        respall  = ""
        resp = ""
        for chunk in chunks:
            text_prompt = {'role': 'user', 'content': f"Сформируй структуру для следующего текста из файла: \n\n{chunk}"}
            prompt2 = prompt.copy()
            for rp in resp_propmps:
                prompt2.append(rp)
            prompt2.append(text_prompt)
            resp = self._gate().request(prompt2)
            resp_propmps.append( {'role': 'assistant', 'content': f'Предыдущее состояние результирующей структуры: {resp}'})
            respall += "============="+resp
            #print(resp, flush=True)
        return resp

    def split_into_chunks(self, text, chunk_size):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def get_pydantics(self, *cls):
        source_code = "\n\n".join(self._get_class_source(c) for c in cls)

        pydantic = f"""
                Ниже pydantic-классы для текущего запроса.
                Корневой класс: ${cls[0].__name__}
    
                ```python
    
                    {source_code}
    
                 ```
                """
        return pydantic

    def get_pydantic(self, cls):
        source_code = self._get_class_source(cls)

        pydantic = f"""
        Вот pydantic-класс для текущего запроса:
        
        ```python
            
            {source_code}
            
         ```
        """
        return pydantic

    def _get_class_source(self, cls):
        try:
            return inspect.getsource(cls)
        except (TypeError, OSError):
            return "Source code not available"
