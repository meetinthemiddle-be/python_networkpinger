
import os

def get_environment_variable(_var):
    candidate_var = os.getenv(str(_var))
    if type(candidate_var).__name__ == 'NoneType':
        print("[!] Environment variable "+ str(_var) + " not found...")
        print("[!] Set it using `export "+ str(_var) + "=\"Sup3r53cretStr1ng\"`")
        return ""
    else:
        return str(candidate_var)
