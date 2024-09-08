
create database almoxarifado;
use almoxarifado;

create table materiais(
codigo_mat int primary key not null,
tipo_mat varchar(1),
numero_bp_mat int,
descricao_mat varchar(255),
observacao_mat varchar(255)
);

create table posicao_estoque(
codigo_pos int primary key,
quant_min_pos int,
quant_atual_pos int,
quant_max_pos int,
foreign key  (codigo_pos) references materiais(codigo_mat)
);


create table professor(
registro_prof int primary key,
nome_prof varchar(255),
telefone_prof bigint(14),
usuario_adm_prof varchar(1),
senha_prof varchar(255)
);

create table movimentacao(
numero_mov int primary key,
data_mov date,
hora_mov time,
funcionarios_mov int,
tipo_mov varchar(1),
observacao_mov varchar(255),
foreign key  (funcionarios_mov) references professor(registro_prof)
);

create table iten_retirado(
numero_iten int primary key,
codigo_iten int,
qtde_iten int,
foreign key  (codigo_iten) references materiais(codigo_mat),
foreign key  (numero_iten) references movimentacao(numero_mov)
);
