# IGNIS - DOCUMENTAÇÃO SERVER

## Requisitos

#### - python3(<a href="https://www.python.org/">link</a>)

#### - pip3(<a href="https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3">link</a>)

## Criando ambiente

```bash
python -m venv env
```

## Iniciando ambiente

**Windows**:

```bash
# Em cmd.exe
env\Scripts\activate.bat
# Em PowerShell
env\Scripts\Activate.ps1
```

**Linux**:

```bash
source env/bin/activate
```

---

## Certificando o ambiente

Sempre que for instalar uma dependência com o `pip`, certifique-se de que o ambiente esteja ativado.

## Instalando as dependências

```bash
pip install -r requirements.txt
```
