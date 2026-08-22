# Changelog

## [v4.0.0rc1] - 2026-04-25
### Recriado programa de envio de XMLs automático
- Nova versão funcionando para gerar relatórios, com registro de XMLs não encontrados e envio pelo Telegram
- Configurado inicialmente para funcionar com SmallSoft, novos serão adicionados em atualizações futuras
- Identificado erro na execução após atualização sobre o programa anterior e corrigido

## [v4.0.0.rc2] - 2026-05-20
### Fixed
- Ajustado para vir com o sistema configurado selecionado
- Corrigido janela de reenvio para não fechar o programa após a execução
- Corrigido janela reenvio com o ícone do programa

### Changes
- Configurado para carregar telegram com arquivo TXT
- Adicionado configurações para o sistema Comercial
- Modificado janela de reenvio para usar botão combo
- Janela reenvio agora bloqueia a janela principal
- Adicionado opção para um segundo sistema
- Configurado funcionamento para envio do arquivo da filial
- Criptografado token e chat_id do telegram


## [v4.1.1rc2] - 2026-06-24
### Fixed
- Feito pequenas correções e melhorias
- Corrigido pasta padrão do sistema Comercial
- Removido variável desnecessária
- Removido a possibilidade de selecionar Outro em sistemas por não ter uma configuração para ele

### Changes
- Reescrito o código para melhor manutenção
- Adicionado verificação do sistema instalado para já selecionar
- Adicionado pasta padrão dos sistemas para verificar

## [v4.1.2rc2] - 2026-07-07
### Changes
- Modificado modo de manipular os dados de configuração

### Fixes
- Corrigido execução da cópia do segundo sistema

## [v4.1.3rc2] - 2026-07-29
### Fixes
- Adicionado remoção de notas em contingência
- Corrigido erro ao fazer primeiro envio logo após gravar os dados
- Pequenos ajustes no rodapé do relatório, corrigido informações apresentadas

## [v4.1.4rc2] - 2026-08-22
### Changes
- Otimizado cópia dos arquivos
- Adcionado módulo arquilo_log.py