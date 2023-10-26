import sqlite3

# Classe que representa uma tarefa


class Task:

    def __init__(self, title, description, completed=False):
        self.title = title
        self.description = description
        self.completed = completed

    def __str__(self):
        # Define o status da tarefa com base no valor de 'completed'
        status = 'Status: Concluida' if self.completed else 'Status: Pendente'
        return f'{status}\nTarefa: {self.title}\n{self.description}'

# Classe que gerencia as tarefas e a base do banco de dados


class TaskManager:
    def __init__(self):
        # Conecta ao banco de dados SQLite
        self.conn = sqlite3.connect('tasks.db')
        # Cria no local a tabela de tarefas se ela não existir
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            completed INTEGER
            )
        ''')
        self.conn.commit()

    def create_task(self, title, description):
        cursor = self.conn.cursor()
        # Insere uma nova tarefa na base de dados com o status padrao 'Pendente' (0)
        cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)', (title, description, 0))

    def list_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title, description, completed FROM tasks')
        tasks = cursor.fetchall()
        cursor.close()

        for task in tasks:
            task_id, title, description, completed = task
            # Exibe o numero da tarefa, status, nome e descricao
            status = 'Status: Concluida' if completed else 'Status: Pendente'
            print(f'Numero da Tarefa:{task_id}\n{status}\nTarefa: {title}\nDescrição:{description}')

    def update_task(self, task_id, title, description):
        cursor = self.conn.cursor()
        # Atualiza o nome da tarefa e sua descricao
        cursor.execute('UPDATE tasks SET title=?, description=? WHERE id=?', (title, description, task_id))

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        # Deleta uma tarefa com base no seu Id
        cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))

    def mark_task_as_completed(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT completed FROM tasks WHERE id=?', task_id)
        result = cursor.fetchone()

        if result is not None:
            current_status = result[0]
            new_status = 1 if current_status == 0 else 0
            cursor.execute('UPDATE tasks SET completed= ? WHERE id=?', (new_status, task_id))
            self.conn.commit()
            print('Tarefa marcada como Concluida' if new_status == 1 else 'Tarefa marcada como Pendente')
        else:
            print('Tarefa não encontrada')

    def close_connection(self):
        # Fecha a conecao com o banco de dados
        self.conn.commit()
        self.conn.close()

    def run(self):
        while True:
            print('''
    Gerenciador de Tarefas
    1. Criar Tarefa
    2. Listar Tarefa
    3. Atualizar Tarefa
    4. Marcar tarefa como concluída
    5. Deletar Tarefa
    6. Sair''')

            choice = input('Escolha uma opção: ')

            if choice == '1':
                # Opcao para criar uma nova tarefa
                title = input("Título da tarefa: ")
                description = input("Descrição da tarefa: ")
                self.create_task(title, description)
                print("Tarefa criada com sucesso!")
            elif choice == '2':
                # Opcao para listar as tarefas existentes
                print('Lista de tarefas')
                self.list_tasks()
            elif choice == '3':
                # Opcao para atualizar a tarefa selecionada
                task_id = input('Indice da tarefa a ser atualizada: ')
                title = input('Novo título da tarefa:')
                description = input("Nova descrição da tarefa: ")
                self.update_task(task_id, title, description)
                print('Tarefa atualizada com sucesso')
            elif choice == '4':
                # Opcao para atualizar a tarefa selecionada para o status 'Concluida'
                task_id = input("Índice da tarefa concluída: ")
                self.mark_task_as_completed(task_id)
            elif choice == '5':
                # Opcao para deletar a tarefa selecionada
                task_id = input("Índice da tarefa a ser excluida: ")
                self.delete_task(task_id)
                print('Tarefa excluida com sucesso!')
            elif choice == '6':
                # Opcao para sair e salvar 
                print('Saindo do Gerenciador de Tarefas. Até logo!!')
                self.close_connection()
                break
            else:
                print('Opção invalida, tente uma opção valida por favor.')


if __name__ == '__main__':
    task_manager = TaskManager()
    task_manager.run()
    task_manager.close_connection()
