## CODIFICAÇÃO

- **Nomeação Clara e Descritiva:** Use nomes de variáveis, funções e classes que sejam claros e descritivos. Nomes devem refletir a finalidade e o uso dos elementos do código, e não misture português/inglês.

- **Comentários e Documentação:** Comente seu código onde necessário para explicar a lógica complexa. Mantenha a documentação atualizada e clara para facilitar a compreensão e manutenção futura.

- **Consistência:** Mantenha uma formatação de código consistente, como indentação, espaçamento e estilo de nomenclatura. Utilize ferramentas de formatação automática para garantir consistência.

- **Divisão de Responsabilidades:** Mantenha suas classes e funções com responsabilidades bem definidas. Cada unidade de código deve ter uma única responsabilidade, conforme sugerido pelos princípios SOLID.

- **Tratamento de Exceções:** Implemente um tratamento de exceções robusto para lidar com erros e garantir que o código seja resiliente a falhas inesperadas.

- **Desempenho e Eficiência:** Otimize o código para desempenho e eficiência, mas não à custa da clareza e legibilidade. Evite otimizações prematuras.

- **Gerenciamento de Dependências:** Gerencie dependências de forma cuidadosa e evite adicionar bibliotecas desnecessárias. Mantenha suas dependências atualizadas e seguras.

## Versionamento(GIT)

- **Escreva Mensagens de Commit Claras:** Use mensagens de commit claras e informativas que expliquem o motivo das mudanças. Um formato comum é:

    ```
      [BRANCH][TIPO_DE_COMMIT]: MENSAGEM
      #EX: [SERVER][FEAT]: Comunicação com ESP32
    ```

- **Use Branches**: Crie branches para novas funcionalidades, correções de bugs ou experimentos. Isso mantém o branch principal (geralmente main ou master) estável e limpo.

Como o repositório abrange diferentes escopos, cada um terá sua própria branch:
- Server
- ESP32
- WebApp
