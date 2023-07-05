import customtkinter
import config

from tkinter import messagebox
from controllers.core.sysmas_resource import LoadSysmaResource 


def do_import(parent, project_instace, filename):
    if filename:

        try: 
            loaded_assets = LoadSysmaResource(filename)

        except TypeError:
            messagebox.showerror("XLSX", "Erro ao ler planilha, ou versão não suportada!", parent=parent)
            return False;

        # Disable
        # if loaded_assets.invalid_resources:
        #     report = messagebox.askyesno("Erro na planilha encontrado", "Deseja gerar planilha com os erros?", icon="warning", parent=parent)

            # if report: faça nova planilha de erros dos itens

        if loaded_assets.valid_resources:
            
            # caso a lista de placas/renavam/chassi seja carregada corretamente faça:
            # if loaded_assets.count_resources > 0:
                # merge = messagebox.askyesnocancel("Mesclagem", "Dejesa mesclar aos veículos atuais?", parent=parent)

                # Se nulo não faz nada
                # if not merge is None:

                #     # aqui se True faz merge dos recursos
                #     if merge:
                #         loaded_assets.merge_resources()
                #     else:
                #         loaded_assets.record_resources())

            # else:
                # loaded_assets.record_resources()
            
            loaded_assets.record_resources(project_instace)

            messagebox.showinfo("Sucesso", "Dados importados com sucesso!", parent=parent)

            return True
        else:
            messagebox.showerror("Erro", "Dados não importados!", parent=parent)

        # BaseWindow.open_top_level(self.master, self.toplevel_window, ProgressBar)

    return False