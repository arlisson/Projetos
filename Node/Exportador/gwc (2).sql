-- Adminer 5.3.0 PostgreSQL 17.5 dump

\connect "gwc";

CREATE SEQUENCE analise_relatorio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."analise_relatorio" (
    "id" integer DEFAULT nextval('analise_relatorio_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "origem" enum_analise_relatorio_origem NOT NULL,
    "tipo" enum_analise_relatorio_tipo NOT NULL,
    "status" enum_analise_relatorio_status DEFAULT 'rascunho' NOT NULL,
    "feedback" text,
    "enviado_em" timestamptz,
    "avaliado_em" timestamptz,
    "relatorio_id" integer,
    "tm_relatorio_projeto_id" integer,
    "tm_relatorio_sitio_id" integer,
    "enviado_por_id" integer NOT NULL,
    "avaliado_por_id" integer,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "analise_relatorio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX analise_relatorio_uuid_key ON public.analise_relatorio USING btree (uuid);

CREATE UNIQUE INDEX analise_relatorio_relatorio_id_key ON public.analise_relatorio USING btree (relatorio_id);

CREATE UNIQUE INDEX analise_relatorio_tm_relatorio_projeto_id_key ON public.analise_relatorio USING btree (tm_relatorio_projeto_id);

CREATE UNIQUE INDEX analise_relatorio_tm_relatorio_sitio_id_key ON public.analise_relatorio USING btree (tm_relatorio_sitio_id);

CREATE UNIQUE INDEX analise_relatorio_uuid ON public.analise_relatorio USING btree (uuid);

CREATE INDEX analise_relatorio_status ON public.analise_relatorio USING btree (status);

CREATE INDEX analise_relatorio_origem_tipo ON public.analise_relatorio USING btree (origem, tipo);

CREATE UNIQUE INDEX analise_relatorio_relatorio_id ON public.analise_relatorio USING btree (relatorio_id);

CREATE UNIQUE INDEX analise_relatorio_tm_relatorio_projeto_id ON public.analise_relatorio USING btree (tm_relatorio_projeto_id);

CREATE UNIQUE INDEX analise_relatorio_tm_relatorio_sitio_id ON public.analise_relatorio USING btree (tm_relatorio_sitio_id);


CREATE SEQUENCE arvore_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."arvore" (
    "id" integer DEFAULT nextval('arvore_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "parcela_id" integer,
    "especie_id" integer NOT NULL,
    "tipo_arvore" enum_arvore_tipo_arvore,
    "numero_arvore" integer,
    "numero_fuste" integer,
    "dap_cm" numeric(6,2) NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "deleted_at" timestamptz,
    CONSTRAINT "arvore_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX arvore_uuid_key ON public.arvore USING btree (uuid);

CREATE INDEX arvore_parcela_id ON public.arvore USING btree (parcela_id);

CREATE INDEX arvore_especie_id ON public.arvore USING btree (especie_id);


CREATE SEQUENCE arvore_plantada_dap_10cm_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."arvore_plantada_dap_10cm" (
    "id" integer DEFAULT nextval('arvore_plantada_dap_10cm_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "parcela_id" integer,
    "especie_id" integer NOT NULL,
    "tipo_arvore" enum_arvore_plantada_dap_10cm_tipo_arvore,
    "numero_arvores" integer NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "deleted_at" timestamptz,
    CONSTRAINT "arvore_plantada_dap_10cm_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX arvore_plantada_dap_10cm_uuid_key ON public.arvore_plantada_dap_10cm USING btree (uuid);

CREATE INDEX arvore_plantada_dap_10cm_parcela_id ON public.arvore_plantada_dap_10cm USING btree (parcela_id);

CREATE INDEX arvore_plantada_dap_10cm_especie_id ON public.arvore_plantada_dap_10cm USING btree (especie_id);


CREATE SEQUENCE atividade_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."atividade" (
    "id" integer DEFAULT nextval('atividade_id_seq') NOT NULL,
    "titulo" character varying(45),
    "quantidade_hectares" numeric(10,4),
    "data_inicio" timestamptz,
    "data_estimada_fim" timestamptz,
    "projeto_id" integer NOT NULL,
    CONSTRAINT "atividade_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE banco_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."banco" (
    "id" integer DEFAULT nextval('banco_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "descricao" character varying(100),
    "area" numeric(10,2),
    "projeto_id" integer NOT NULL,
    "sitio_id" integer,
    "poligono_id" integer,
    "estrato_id" integer,
    "tecnica_id" integer NOT NULL,
    "banco_id" integer,
    CONSTRAINT "banco_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX banco_uuid_key ON public.banco USING btree (uuid);


CREATE SEQUENCE categoria_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 3 CACHE 1;

CREATE TABLE "public"."categoria" (
    "id" integer DEFAULT nextval('categoria_id_seq') NOT NULL,
    "descricao" character varying(45) NOT NULL,
    CONSTRAINT "categoria_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE convite_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."convite" (
    "id" integer DEFAULT nextval('convite_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "email" character varying(255) NOT NULL,
    "role" enum_convite_role DEFAULT 'user' NOT NULL,
    "vcode" uuid,
    "enviado_em" timestamptz NOT NULL,
    "aceito_em" timestamptz,
    "criado_por_admin_uuid" uuid,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "convite_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX convite_uuid_key ON public.convite USING btree (uuid);

CREATE UNIQUE INDEX convite_email_key ON public.convite USING btree (email);


CREATE SEQUENCE coordenadas_pacto_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."coordenadas_pacto" (
    "id" integer DEFAULT nextval('coordenadas_pacto_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "parcela_id" integer,
    "plot_id" character varying(64),
    "vertice" integer,
    "x_sirgas2000_utm23s" numeric(10,2),
    "y_sirgas2000_utm23s" numeric(10,2),
    "notes" text,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "deleted_at" timestamptz,
    CONSTRAINT "coordenadas_pacto_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX coordenadas_pacto_uuid_key ON public.coordenadas_pacto USING btree (uuid);

CREATE INDEX coordenadas_pacto_parcela_id ON public.coordenadas_pacto USING btree (parcela_id);


CREATE SEQUENCE coordenadas_ppc_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."coordenadas_ppc" (
    "id" integer DEFAULT nextval('coordenadas_ppc_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "parcela_id" integer,
    "latitude_s_i_r_g_a_s2000" numeric(9,6),
    "longitude_s_i_r_g_a_s2000" numeric(9,6),
    "latitude_w_g_s84" numeric(9,6),
    "longitude_w_g_s84" numeric(9,6),
    "elevacao" numeric(8,2),
    "data_hora" timestamptz,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "deleted_at" timestamptz,
    CONSTRAINT "coordenadas_ppc_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX coordenadas_ppc_uuid_key ON public.coordenadas_ppc USING btree (uuid);

CREATE INDEX coordenadas_ppc_parcela_id ON public.coordenadas_ppc USING btree (parcela_id);


CREATE SEQUENCE demografia_dos_dias_uteis_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."demografia_dos_dias_uteis" (
    "id" integer DEFAULT nextval('demografia_dos_dias_uteis_id_seq') NOT NULL,
    "tipo" character varying(45) DEFAULT 'voluntario' NOT NULL,
    "categoria" character varying(45),
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "demografia_dos_dias_uteis_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE TABLE "public"."demografia_dos_dias_uteis_has_etnia" (
    "demografia_dos_dias_uteis_id" integer NOT NULL,
    "etnia_id" integer NOT NULL,
    "quantidade" integer,
    CONSTRAINT "demografia_dos_dias_uteis_has_etnia_pkey" PRIMARY KEY ("demografia_dos_dias_uteis_id", "etnia_id")
)
WITH (oids = false);


CREATE TABLE "public"."demografia_dos_dias_uteis_has_faixa_etaria" (
    "demografia_dos_dias_uteis_id" integer NOT NULL,
    "faixa_etaria_id" integer NOT NULL,
    "quantidade" integer,
    CONSTRAINT "demografia_dos_dias_uteis_has_faixa_etaria_pkey" PRIMARY KEY ("demografia_dos_dias_uteis_id", "faixa_etaria_id")
)
WITH (oids = false);


CREATE TABLE "public"."demografia_dos_dias_uteis_has_genero" (
    "demografia_dos_dias_uteis_id" integer NOT NULL,
    "genero_id" integer NOT NULL,
    "quantidade" integer,
    CONSTRAINT "demografia_dos_dias_uteis_has_genero_pkey" PRIMARY KEY ("demografia_dos_dias_uteis_id", "genero_id")
)
WITH (oids = false);


CREATE SEQUENCE diagnostico_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."diagnostico" (
    "id" integer DEFAULT nextval('diagnostico_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "descricao" character varying(1000),
    "implantacao_id" integer NOT NULL,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "diagnostico_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX diagnostico_uuid_key ON public.diagnostico USING btree (uuid);


CREATE SEQUENCE docs_imovel_rural_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."docs_imovel_rural" (
    "id" integer DEFAULT nextval('docs_imovel_rural_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "tag" character varying(45) NOT NULL,
    "file" character varying(255) NOT NULL,
    "imovel_rural_id" integer NOT NULL,
    CONSTRAINT "docs_imovel_rural_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

COMMENT ON COLUMN "public"."docs_imovel_rural"."tag" IS 'Tipo do documento: ccir, car, certificado, escritura, shapefile_total, shapefile_restauracao, tac';

COMMENT ON COLUMN "public"."docs_imovel_rural"."file" IS 'Conteúdo do documento (arquivo binário)';

CREATE UNIQUE INDEX docs_imovel_rural_uuid_key ON public.docs_imovel_rural USING btree (uuid);


CREATE SEQUENCE email_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."email" (
    "id" integer DEFAULT nextval('email_id_seq') NOT NULL,
    "email" character varying(80) NOT NULL,
    CONSTRAINT "email_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE especie_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 895 CACHE 1;

CREATE TABLE "public"."especie" (
    "id" integer DEFAULT nextval('especie_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "nome" character varying(100),
    "nome_cientifico" character varying(180),
    CONSTRAINT "especie_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX especie_uuid_key ON public.especie USING btree (uuid);


CREATE SEQUENCE estado_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 28 CACHE 1;

CREATE TABLE "public"."estado" (
    "id" integer DEFAULT nextval('estado_id_seq') NOT NULL,
    "sigla" character varying(45),
    "nome" character varying(45),
    CONSTRAINT "estado_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX estado_sigla_key ON public.estado USING btree (sigla);

CREATE UNIQUE INDEX estado_nome_key ON public.estado USING btree (nome);


CREATE SEQUENCE estrato_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."estrato" (
    "id" integer DEFAULT nextval('estrato_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "codigo" character varying(45) NOT NULL,
    "area" numeric(10,2),
    CONSTRAINT "estrato_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX estrato_uuid_key ON public.estrato USING btree (uuid);

CREATE UNIQUE INDEX estrato_codigo_key ON public.estrato USING btree (codigo);


CREATE SEQUENCE etnia_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 9 CACHE 1;

CREATE TABLE "public"."etnia" (
    "id" integer DEFAULT nextval('etnia_id_seq') NOT NULL,
    "codigo" character varying(40) NOT NULL,
    "descricao" character varying(120) NOT NULL,
    "ordem" smallint DEFAULT '0' NOT NULL,
    "ativo" boolean DEFAULT true NOT NULL,
    CONSTRAINT "etnia_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX etnia_codigo_key ON public.etnia USING btree (codigo);

CREATE UNIQUE INDEX etnia_codigo ON public.etnia USING btree (codigo);


CREATE SEQUENCE evidencia_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."evidencia" (
    "id" integer DEFAULT nextval('evidencia_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "descricao" character varying(1000),
    "registro" character varying(200),
    "fase" character varying(100),
    "relatorio_id" integer NOT NULL,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "evidencia_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX evidencia_uuid_key ON public.evidencia USING btree (uuid);


CREATE SEQUENCE faixa_etaria_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 4 CACHE 1;

CREATE TABLE "public"."faixa_etaria" (
    "id" integer DEFAULT nextval('faixa_etaria_id_seq') NOT NULL,
    "codigo" character varying(40) NOT NULL,
    "descricao" character varying(120) NOT NULL,
    "faixa_min" smallint,
    "faixa_max" smallint,
    "ordem" smallint DEFAULT '0' NOT NULL,
    "ativo" boolean DEFAULT true NOT NULL,
    CONSTRAINT "faixa_etaria_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX faixa_etaria_codigo_key ON public.faixa_etaria USING btree (codigo);

CREATE UNIQUE INDEX faixa_etaria_codigo ON public.faixa_etaria USING btree (codigo);


CREATE SEQUENCE genero_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 6 CACHE 1;

CREATE TABLE "public"."genero" (
    "id" integer DEFAULT nextval('genero_id_seq') NOT NULL,
    "codigo" character varying(40) NOT NULL,
    "descricao" character varying(120) NOT NULL,
    "ordem" smallint DEFAULT '0' NOT NULL,
    "ativo" boolean DEFAULT true NOT NULL,
    CONSTRAINT "genero_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX genero_codigo_key ON public.genero USING btree (codigo);

CREATE UNIQUE INDEX genero_codigo ON public.genero USING btree (codigo);


CREATE TABLE "geography_columns" ("f_table_catalog" name, "f_table_schema" name, "f_table_name" name, "f_geography_column" name, "coord_dimension" integer, "srid" integer, "type" text);


CREATE TABLE "geometry_columns" ("f_table_catalog" character varying(256), "f_table_schema" name, "f_table_name" name, "f_geometry_column" name, "coord_dimension" integer, "srid" integer, "type" character varying(30));


CREATE SEQUENCE imovel_rural_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."imovel_rural" (
    "id" integer DEFAULT nextval('imovel_rural_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "criado_por" integer,
    "nome_fazenda_ou_uc" character varying(100),
    "categoria_id" integer NOT NULL,
    "area_total_da_fazenda_ha" numeric(10,2),
    "area_destinada_ao_projeto_de_agricultura_sustentavel" numeric(10,2),
    "localizacao_id" integer NOT NULL,
    "numero_de_cabecas_de_gado_criadas" integer,
    "cultivos_realizados" character varying(255),
    "ccir" character varying(100),
    "car_cefir_numero" character varying(100),
    "propriedade_possui_certificacao" boolean,
    "area_supressao_autorizada" boolean,
    "possui_passivo_ambiental" boolean,
    "supressao_apos_2008" boolean,
    "orgao_solicitou_recuperacao" boolean,
    "possui_tac" boolean,
    "tac" bytea,
    CONSTRAINT "imovel_rural_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX imovel_rural_uuid_key ON public.imovel_rural USING btree (uuid);


CREATE SEQUENCE implantacao_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."implantacao" (
    "id" integer DEFAULT nextval('implantacao_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "data_inicio" timestamptz,
    "data_fim" timestamptz,
    "espacamento" character varying(200),
    "meta_arvores" integer,
    "meta_cobertura_copa" numeric(10,4),
    "taxa_sobrevivencia" numeric(10,4),
    "regenerantes" integer,
    "taxa_mortalidade" numeric(10,4),
    "banco_id" integer NOT NULL,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    "relatorio_id" integer,
    CONSTRAINT "implantacao_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX implantacao_uuid_key ON public.implantacao USING btree (uuid);


CREATE SEQUENCE item_implantacao_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."item_implantacao" (
    "id" integer DEFAULT nextval('item_implantacao_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "implantacao_id" integer NOT NULL,
    "relatorio_id" integer NOT NULL,
    "hectares_preparados" numeric(10,4) NOT NULL,
    "hectares_plantados" numeric(10,4),
    "hectares_semeados" numeric(10,4),
    "arvores_plantadas" integer,
    "sementes_plantadas" integer,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "item_implantacao_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX item_implantacao_uuid_key ON public.item_implantacao USING btree (uuid);


CREATE SEQUENCE item_manutencao_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."item_manutencao" (
    "id" integer DEFAULT nextval('item_manutencao_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "implantacao_id" integer NOT NULL,
    "relatorio_id" integer NOT NULL,
    "hectares_manutencao" numeric(10,4) NOT NULL,
    "hectares_replantados" numeric(10,4),
    "individuos_replantados" integer,
    "especies_replantados" integer,
    "especies_invasoras" integer,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "item_manutencao_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX item_manutencao_uuid_key ON public.item_manutencao USING btree (uuid);


CREATE SEQUENCE item_monitoramento_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."item_monitoramento" (
    "id" integer DEFAULT nextval('item_monitoramento_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "implantacao_id" integer NOT NULL,
    "relatorio_id" integer NOT NULL,
    "individuos_plantados" integer NOT NULL,
    "estimativa_individuos_hectar" integer,
    "individuos_hectar" integer,
    "parcelas_controle" integer,
    "parcelas_monitoramento" integer,
    "estimativa_co2_sequestrado" numeric(10,4),
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "item_monitoramento_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX item_monitoramento_uuid_key ON public.item_monitoramento USING btree (uuid);


CREATE SEQUENCE localizacao_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."localizacao" (
    "id" integer DEFAULT nextval('localizacao_id_seq') NOT NULL,
    "logradouro" character varying(80),
    "numero" character varying(10),
    "complemento" character varying(45),
    "bairro" character varying(45),
    "cep" character varying(10),
    "municipio_id" integer NOT NULL,
    CONSTRAINT "localizacao_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE logs_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."logs" (
    "id" integer DEFAULT nextval('logs_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "user_uuid" character varying(255) DEFAULT 'anonymous' NOT NULL,
    "url" character varying(255) NOT NULL,
    "role" character varying(255) NOT NULL,
    "status_code" integer,
    "ip" character varying(255) NOT NULL,
    "action" character varying(255) NOT NULL,
    "method" character varying(255) NOT NULL,
    "model" character varying(255) NOT NULL,
    "data" jsonb,
    "error" jsonb,
    "issuer" jsonb,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "logs_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX logs_uuid_key ON public.logs USING btree (uuid);


CREATE SEQUENCE manejo_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 5 CACHE 1;

CREATE TABLE "public"."manejo" (
    "id" integer DEFAULT nextval('manejo_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "titulo" character varying(45),
    CONSTRAINT "manejo_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX manejo_uuid_key ON public.manejo USING btree (uuid);


CREATE SEQUENCE matricula_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."matricula" (
    "id" integer DEFAULT nextval('matricula_id_seq') NOT NULL,
    "inscricao" character varying(100) NOT NULL,
    "imovel_rural_id" integer NOT NULL,
    CONSTRAINT "matricula_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE membros_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."membros" (
    "id" integer DEFAULT nextval('membros_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "funcao" character varying(45) NOT NULL,
    "pessoa_id" integer NOT NULL,
    "projeto_id" integer NOT NULL,
    CONSTRAINT "membros_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

COMMENT ON COLUMN "public"."membros"."funcao" IS 'Função: responsavel_tecnico, instituicao_parceira, organizacao_responsavel';

CREATE UNIQUE INDEX membros_uuid_key ON public.membros USING btree (uuid);


CREATE SEQUENCE metodologia_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."metodologia" (
    "id" integer DEFAULT nextval('metodologia_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "nome" character varying(100),
    CONSTRAINT "metodologia_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX metodologia_uuid_key ON public.metodologia USING btree (uuid);


CREATE SEQUENCE midia_adicional_parcela_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."midia_adicional_parcela" (
    "id" integer DEFAULT nextval('midia_adicional_parcela_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "parcela_id" integer,
    "foto_nome" character varying(160),
    "foto_url" character varying(1024),
    "arquivo_nome" character varying(160),
    "arquivo_url" character varying(1024),
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "deleted_at" timestamptz,
    CONSTRAINT "midia_adicional_parcela_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX midia_adicional_parcela_uuid_key ON public.midia_adicional_parcela USING btree (uuid);

CREATE INDEX midia_adicional_parcela_parcela_id ON public.midia_adicional_parcela USING btree (parcela_id);


CREATE SEQUENCE monitoramento_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."monitoramento" (
    "id" integer DEFAULT nextval('monitoramento_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "id_sitio" character varying(64) NOT NULL,
    "tipo_sitio" character varying(64) NOT NULL,
    "data_coleta" date NOT NULL,
    "pais" character varying(64) NOT NULL,
    "periodo_amostragem" character varying(64) NOT NULL,
    "hora_inicio" time without time zone,
    "hora_fim" time without time zone,
    "responsavel_coleta_id" integer NOT NULL,
    "organizacao_id" integer,
    "cobertura_copa_pct" numeric(5,2),
    "invasoras_nivel" enum_monitoramento_invasoras_nivel,
    "nativas_plantadas" integer,
    "invasoras_arboreas" integer,
    "fertilidade_solo" enum_monitoramento_fertilidade_solo,
    "compactacao_solo" enum_monitoramento_compactacao_solo,
    "conservacao_solo31" enum_monitoramento_conservacao_solo31,
    "conservacao_solo32" enum_monitoramento_conservacao_solo32,
    "outros_fatores_edaficos" text,
    "fogo_ocorrencia" boolean,
    "fogo_foto_url" character varying(1024),
    "gado_presenca" boolean,
    "ataque_formigas" boolean,
    "observacao_geral" text,
    "observacao_parcela30x15" text,
    "observacao_subparcela3x3" text,
    "observacao_adicional" text,
    "submission_time" timestamptz,
    "status" character varying(32) DEFAULT 'submitted_via_web',
    "submitted_by_id" integer,
    "version" character varying(64),
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "monitoramento_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX monitoramento_uuid_key ON public.monitoramento USING btree (uuid);

CREATE UNIQUE INDEX monitoramento_id_sitio_key ON public.monitoramento USING btree (id_sitio);

CREATE UNIQUE INDEX monitoramento_uuid ON public.monitoramento USING btree (uuid);

CREATE UNIQUE INDEX monitoramento_id_sitio ON public.monitoramento USING btree (id_sitio);

CREATE INDEX monitoramento_responsavel_coleta_id ON public.monitoramento USING btree (responsavel_coleta_id);

CREATE INDEX monitoramento_organizacao_id ON public.monitoramento USING btree (organizacao_id);

CREATE INDEX monitoramento_status ON public.monitoramento USING btree (status);


CREATE SEQUENCE muda_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."muda" (
    "id" integer DEFAULT nextval('muda_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "quantidade" integer,
    "objetivo" character varying(45),
    "forma_de_aquisicao" character varying(45),
    "mortalidade" integer,
    "viveiro_id" integer NOT NULL,
    "relatorio_id" integer NOT NULL,
    "especie_id" integer,
    CONSTRAINT "muda_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX muda_uuid_key ON public.muda USING btree (uuid);


CREATE SEQUENCE municipio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 5596 CACHE 1;

CREATE TABLE "public"."municipio" (
    "id" integer DEFAULT nextval('municipio_id_seq') NOT NULL,
    "nome" character varying(45),
    "estado_id" integer NOT NULL,
    CONSTRAINT "municipio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE parcela_monitoramento_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."parcela_monitoramento" (
    "id" integer DEFAULT nextval('parcela_monitoramento_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "id_parcela" character varying(64) NOT NULL,
    "tipo_parcela" enum_parcela_monitoramento_tipo_parcela NOT NULL,
    "estrato" character varying(64),
    "arvores_d_a_p_presentes" boolean DEFAULT false NOT NULL,
    "numero_reamostragens" integer,
    "descricao_espacamento_plantio" text,
    "monitoramento_id" integer,
    "vertices" jsonb DEFAULT '[]' NOT NULL,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "parcela_monitoramento_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX parcela_monitoramento_uuid_key ON public.parcela_monitoramento USING btree (uuid);

CREATE UNIQUE INDEX parcela_monitoramento_id_parcela_key ON public.parcela_monitoramento USING btree (id_parcela);

CREATE UNIQUE INDEX parcela_monitoramento_id_parcela ON public.parcela_monitoramento USING btree (id_parcela);

CREATE INDEX parcela_monitoramento_monitoramento_id ON public.parcela_monitoramento USING btree (monitoramento_id);


CREATE SEQUENCE pessoa_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."pessoa" (
    "uuid" uuid NOT NULL,
    "id" integer DEFAULT nextval('pessoa_id_seq') NOT NULL,
    "usuario_id" integer,
    CONSTRAINT "pessoa_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX pessoa_uuid_key ON public.pessoa USING btree (uuid);


CREATE SEQUENCE pessoa_fisica_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."pessoa_fisica" (
    "id" integer DEFAULT nextval('pessoa_fisica_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "cpf" character varying(45),
    "nome" character varying(45) NOT NULL,
    "pessoa_id" integer NOT NULL,
    CONSTRAINT "pessoa_fisica_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX pessoa_fisica_uuid_key ON public.pessoa_fisica USING btree (uuid);


CREATE SEQUENCE pessoa_juridica_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."pessoa_juridica" (
    "id" integer DEFAULT nextval('pessoa_juridica_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "cnpj" character varying(45),
    "razao_social" character varying(45) NOT NULL,
    "pessoa_id" integer NOT NULL,
    CONSTRAINT "pessoa_juridica_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX pessoa_juridica_uuid_key ON public.pessoa_juridica USING btree (uuid);


CREATE TABLE "public"."pessoa_tem_email" (
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "email_id" integer NOT NULL,
    "pessoa_id" integer NOT NULL,
    CONSTRAINT "pessoa_tem_email_pkey" PRIMARY KEY ("email_id", "pessoa_id")
)
WITH (oids = false);


CREATE TABLE "public"."pessoa_tem_telefone" (
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "telefone_id" integer NOT NULL,
    "pessoa_id" integer NOT NULL,
    CONSTRAINT "pessoa_tem_telefone_pkey" PRIMARY KEY ("telefone_id", "pessoa_id")
)
WITH (oids = false);


CREATE SEQUENCE poligono_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."poligono" (
    "id" integer DEFAULT nextval('poligono_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "codigo" character varying(45) NOT NULL,
    "area" numeric(10,2),
    "sitio_id" integer NOT NULL,
    "shape" geometry,
    CONSTRAINT "poligono_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX poligono_uuid_key ON public.poligono USING btree (uuid);


CREATE SEQUENCE projeto_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."projeto" (
    "id" integer DEFAULT nextval('projeto_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "codigo" character varying(45),
    "titulo" character varying(80),
    "descricao" text,
    "data_inicio" timestamptz,
    "data_estimada_fim" timestamptz,
    "criado_por" integer,
    CONSTRAINT "projeto_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX projeto_uuid_key ON public.projeto USING btree (uuid);


CREATE SEQUENCE projeto_tem_especie_planta_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."projeto_tem_especie_planta" (
    "id" integer DEFAULT nextval('projeto_tem_especie_planta_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "quantidade" integer,
    "manejo_id" integer,
    "especie_id" integer NOT NULL,
    "projeto_id" integer NOT NULL,
    CONSTRAINT "projeto_tem_especie_planta_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX projeto_tem_especie_planta_uuid_key ON public.projeto_tem_especie_planta USING btree (uuid);


CREATE SEQUENCE projeto_tem_imovel_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."projeto_tem_imovel" (
    "id" integer DEFAULT nextval('projeto_tem_imovel_id_seq') NOT NULL,
    "area_destinada_restauracao" numeric(12,2) DEFAULT '0',
    "projeto_id" integer NOT NULL,
    "imovel_rural_id" integer NOT NULL,
    CONSTRAINT "projeto_tem_imovel_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE projeto_tem_metodologia_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."projeto_tem_metodologia" (
    "id" integer DEFAULT nextval('projeto_tem_metodologia_id_seq') NOT NULL,
    "projeto_id" integer NOT NULL,
    "metodologia_id" integer NOT NULL,
    CONSTRAINT "projeto_tem_metodologia_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE relatorio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."relatorio" (
    "id" integer DEFAULT nextval('relatorio_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "titulo" character varying(120),
    "data_inicio" timestamptz,
    "data_fim" timestamptz,
    "resumo_ocorrido" character varying(1000),
    "resumo_proximos_passos" character varying(1000),
    "tipo" character varying(20),
    "projeto_id" integer NOT NULL,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "relatorio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX relatorio_uuid_key ON public.relatorio USING btree (uuid);


CREATE SEQUENCE relatorio_projeto_has_demografia_dos_dias_uteis_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."relatorio_projeto_has_demografia_dos_dias_uteis" (
    "id" integer DEFAULT nextval('relatorio_projeto_has_demografia_dos_dias_uteis_id_seq') NOT NULL,
    "relatorio_projeto_id" integer NOT NULL,
    "demografia_dos_dias_uteis_id" integer NOT NULL,
    CONSTRAINT "relatorio_projeto_has_demografia_dos_dias_uteis_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE relatorio_sitio_has_demografia_dos_dias_uteis_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."relatorio_sitio_has_demografia_dos_dias_uteis" (
    "id" integer DEFAULT nextval('relatorio_sitio_has_demografia_dos_dias_uteis_id_seq') NOT NULL,
    "relatorio_sitio_id" integer NOT NULL,
    "demografia_dos_dias_uteis_id" integer NOT NULL,
    CONSTRAINT "relatorio_sitio_has_demografia_dos_dias_uteis_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE responsavel_imovel_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."responsavel_imovel" (
    "id" integer DEFAULT nextval('responsavel_imovel_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "funcao" character varying(45),
    "pessoa_id" integer NOT NULL,
    "imovel_rural_id" integer NOT NULL,
    CONSTRAINT "responsavel_imovel_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX responsavel_imovel_uuid_key ON public.responsavel_imovel USING btree (uuid);


CREATE SEQUENCE semente_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."semente" (
    "id" integer DEFAULT nextval('semente_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "nome" character varying(45),
    "descricao" character varying(100),
    "quantidade" numeric(10,2),
    "forma_de_aquisicao" character varying(45),
    "especie_id" integer NOT NULL,
    CONSTRAINT "semente_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX semente_uuid_key ON public.semente USING btree (uuid);


CREATE SEQUENCE sitio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."sitio" (
    "id" integer DEFAULT nextval('sitio_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "area" numeric(10,2),
    "imovel_rural_id" integer NOT NULL,
    "shape" geometry,
    CONSTRAINT "sitio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX sitio_uuid_key ON public.sitio USING btree (uuid);


CREATE TABLE "public"."spatial_ref_sys" (
    "srid" integer NOT NULL,
    "auth_name" character varying(256),
    "auth_srid" integer,
    "srtext" character varying(2048),
    "proj4text" character varying(2048),
    CONSTRAINT "spatial_ref_sys_pkey" PRIMARY KEY ("srid"),
    CONSTRAINT "spatial_ref_sys_srid_check" CHECK ((srid > 0) AND (srid <= 998999))
)
WITH (oids = false);


CREATE SEQUENCE subparcela_arvore_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."subparcela_arvore" (
    "id" integer DEFAULT nextval('subparcela_arvore_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "subparcela_id" integer,
    "especie_id" integer NOT NULL,
    "tipo_arvore" enum_subparcela_arvore_tipo_arvore,
    "numero_arvores_especie" integer NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "deleted_at" timestamptz,
    CONSTRAINT "subparcela_arvore_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX subparcela_arvore_uuid_key ON public.subparcela_arvore USING btree (uuid);

CREATE INDEX subparcela_arvore_subparcela_id ON public.subparcela_arvore USING btree (subparcela_id);

CREATE INDEX subparcela_arvore_especie_id ON public.subparcela_arvore USING btree (especie_id);


CREATE SEQUENCE subparcela_monitoramento_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."subparcela_monitoramento" (
    "id" integer DEFAULT nextval('subparcela_monitoramento_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "id_subparcela" character varying(64) NOT NULL,
    "parcela_id" integer,
    "centroide_latitude" numeric(9,6) NOT NULL,
    "centroide_longitude" numeric(9,6) NOT NULL,
    "centroide_altitude" numeric(8,2),
    "centroide_precisao" numeric(6,2),
    "foto_url" character varying(1024),
    "descricao_localizacao" text,
    "numero_amostragens" integer,
    "arvores_d_a_p_1_9__presentes" boolean DEFAULT false NOT NULL,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "subparcela_monitoramento_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX subparcela_monitoramento_uuid_key ON public.subparcela_monitoramento USING btree (uuid);

CREATE INDEX subparcela_monitoramento_parcela_id ON public.subparcela_monitoramento USING btree (parcela_id);

CREATE UNIQUE INDEX subparcela_monitoramento_id_subparcela_parcela_id ON public.subparcela_monitoramento USING btree (id_subparcela, parcela_id);


CREATE SEQUENCE tecnica_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tecnica" (
    "id" integer DEFAULT nextval('tecnica_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "titulo" character varying(100),
    "metodologia_id" integer NOT NULL,
    CONSTRAINT "tecnica_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tecnica_uuid_key ON public.tecnica USING btree (uuid);


CREATE SEQUENCE telefone_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."telefone" (
    "id" integer DEFAULT nextval('telefone_id_seq') NOT NULL,
    "numero" character varying(45) NOT NULL,
    "ddd" integer NOT NULL,
    CONSTRAINT "telefone_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE terms_of_use_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."terms_of_use" (
    "id" integer DEFAULT nextval('terms_of_use_id_seq') NOT NULL,
    "user_id" integer NOT NULL,
    "version" character varying(255) DEFAULT 'v1.0' NOT NULL,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "terms_of_use_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE tipo_uso_solo_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tipo_uso_solo" (
    "id" integer DEFAULT nextval('tipo_uso_solo_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "titulo" character varying(120) NOT NULL,
    "ativo" boolean DEFAULT true NOT NULL,
    CONSTRAINT "tipo_uso_solo_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tipo_uso_solo_uuid_key ON public.tipo_uso_solo USING btree (uuid);

CREATE UNIQUE INDEX tipo_uso_solo_titulo_key ON public.tipo_uso_solo USING btree (titulo);

CREATE UNIQUE INDEX tipo_uso_solo_uuid ON public.tipo_uso_solo USING btree (uuid);

CREATE INDEX tipo_uso_solo_titulo ON public.tipo_uso_solo USING btree (titulo);


CREATE SEQUENCE tm_disturbio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_disturbio" (
    "id" integer DEFAULT nextval('tm_disturbio_id_seq') NOT NULL,
    "titulo" character varying(120),
    "descricao" text,
    "relatorio_sitio_id" integer NOT NULL,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "tm_disturbio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX tm_disturbio_relatorio_sitio_id ON public.tm_disturbio USING btree (relatorio_sitio_id);


CREATE SEQUENCE tm_evidencias_e_registro_fotografico_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_evidencias_e_registro_fotografico" (
    "id" integer DEFAULT nextval('tm_evidencias_e_registro_fotografico_id_seq') NOT NULL,
    "evidencias" character varying(255),
    "link_registro_fotografico" character varying(2048),
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    CONSTRAINT "tm_evidencias_e_registro_fotografico_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX tm_evidencias_e_registro_fotografico_evidencias ON public.tm_evidencias_e_registro_fotografico USING btree (evidencias);


CREATE SEQUENCE tm_geometria_sitio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1;

CREATE TABLE "public"."tm_geometria_sitio" (
    "id" bigint DEFAULT nextval('tm_geometria_sitio_id_seq') NOT NULL,
    "nome_arquivo" character varying(255) NOT NULL,
    "tipo_geometria" character varying(50),
    "geometria" geometry NOT NULL,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    "tm_sitio_id" integer,
    CONSTRAINT "tm_geometria_sitio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX tm_geometria_sitio_tm_sitio_id ON public.tm_geometria_sitio USING btree (tm_sitio_id);

CREATE INDEX tm_geometria_sitio_geometria ON public.tm_geometria_sitio USING gist (geometria);


CREATE TABLE "public"."tm_membro_projeto" (
    "projeto_id" integer NOT NULL,
    "pessoa_id" integer NOT NULL,
    "funcao" character varying(60),
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    CONSTRAINT "tm_membro_projeto_pkey" PRIMARY KEY ("projeto_id", "pessoa_id")
)
WITH (oids = false);

CREATE INDEX tm_membro_projeto_projeto_id ON public.tm_membro_projeto USING btree (projeto_id);

CREATE INDEX tm_membro_projeto_pessoa_id ON public.tm_membro_projeto USING btree (pessoa_id);

CREATE INDEX tm_membro_projeto_funcao ON public.tm_membro_projeto USING btree (funcao);


CREATE SEQUENCE tm_projeto_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_projeto" (
    "id" integer DEFAULT nextval('tm_projeto_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "nome" character varying(255) NOT NULL,
    "organizacao" character varying(255),
    "status" character varying(50),
    "hectares_objetivo" numeric(10,2),
    "taxa_sobrevivencia" integer,
    "meta_cobertura_cinco_anos" integer,
    "data_fim_plantio" date,
    "data_inicio_plantio" date,
    "continente" character varying(100),
    "pais" character varying(3),
    "descricao_timeline" text,
    "historico" text,
    "arquivos_adicionais" text,
    "dados_extras" text,
    "criado_por" integer,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "tm_projeto_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_projeto_uuid_key ON public.tm_projeto USING btree (uuid);

CREATE UNIQUE INDEX tm_projeto_uuid ON public.tm_projeto USING btree (uuid);

CREATE INDEX tm_projeto_nome ON public.tm_projeto USING btree (nome);

CREATE INDEX tm_projeto_status ON public.tm_projeto USING btree (status);

CREATE INDEX tm_projeto_pais ON public.tm_projeto USING btree (pais);

CREATE INDEX tm_projeto_continente ON public.tm_projeto USING btree (continente);

CREATE INDEX tm_projeto_data_inicio_plantio ON public.tm_projeto USING btree (data_inicio_plantio);

CREATE INDEX tm_projeto_data_fim_plantio ON public.tm_projeto USING btree (data_fim_plantio);


CREATE SEQUENCE tm_projeto_tem_especie_arvore_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_projeto_tem_especie_arvore" (
    "id" integer DEFAULT nextval('tm_projeto_tem_especie_arvore_id_seq') NOT NULL,
    "tm_projeto_id" integer NOT NULL,
    "especie_id" integer NOT NULL,
    "projeto_id" integer,
    CONSTRAINT "tm_projeto_tem_especie_arvore_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_projeto_tem_especie_arvore_tm_projeto_id_especie_id ON public.tm_projeto_tem_especie_arvore USING btree (tm_projeto_id, especie_id);


CREATE SEQUENCE tm_projeto_tem_tecnica_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_projeto_tem_tecnica" (
    "id" integer DEFAULT nextval('tm_projeto_tem_tecnica_id_seq') NOT NULL,
    "tm_projeto_id" integer NOT NULL,
    "tecnica_id" integer NOT NULL,
    "projeto_id" integer,
    CONSTRAINT "tm_projeto_tem_tecnica_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_projeto_tem_tecnica_tm_projeto_id_tecnica_id ON public.tm_projeto_tem_tecnica USING btree (tm_projeto_id, tecnica_id);


CREATE SEQUENCE tm_projeto_tem_tipo_uso_solo_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_projeto_tem_tipo_uso_solo" (
    "id" integer DEFAULT nextval('tm_projeto_tem_tipo_uso_solo_id_seq') NOT NULL,
    "tm_projeto_id" integer NOT NULL,
    "tipo_uso_solo_id" integer NOT NULL,
    "projeto_id" integer,
    CONSTRAINT "tm_projeto_tem_tipo_uso_solo_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_projeto_tem_tipo_uso_solo_tm_projeto_id_tipo_uso_solo_id ON public.tm_projeto_tem_tipo_uso_solo USING btree (tm_projeto_id, tipo_uso_solo_id);


CREATE SEQUENCE tm_relatorio_projeto_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_relatorio_projeto" (
    "id" integer DEFAULT nextval('tm_relatorio_projeto_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "projeto_id" integer NOT NULL,
    "data_prazo" timestamptz,
    "titulo" character varying(255),
    "narrativa_tecnica" text,
    "narrativa_publica" text,
    "total_mudas_produzidas_relatorio" integer,
    "total_parceiros_restauracao_unicos" integer,
    "arquivo" text,
    "outros_documentos_adicionais" text,
    "dados_extras" text,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "tm_relatorio_projeto_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_relatorio_projeto_uuid_key ON public.tm_relatorio_projeto USING btree (uuid);

CREATE UNIQUE INDEX tm_relatorio_projeto_uuid ON public.tm_relatorio_projeto USING btree (uuid);

CREATE INDEX tm_relatorio_projeto_projeto_id ON public.tm_relatorio_projeto USING btree (projeto_id);


CREATE SEQUENCE tm_relatorio_projeto_photos_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_relatorio_projeto_photos" (
    "id" integer DEFAULT nextval('tm_relatorio_projeto_photos_id_seq') NOT NULL,
    "relatorio_id" integer NOT NULL,
    "evidencia_id" integer NOT NULL,
    CONSTRAINT "tm_relatorio_projeto_photos_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX tm_relatorio_projeto_photos_relatorio_id ON public.tm_relatorio_projeto_photos USING btree (relatorio_id);

CREATE INDEX tm_relatorio_projeto_photos_evidencia_id ON public.tm_relatorio_projeto_photos USING btree (evidencia_id);


CREATE SEQUENCE tm_relatorio_sitio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_relatorio_sitio" (
    "id" integer DEFAULT nextval('tm_relatorio_sitio_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "data_de_vencimento" date,
    "total_arvores_plantadas" integer,
    "total_sementes_plantadas" integer,
    "titulo" character varying(255),
    "narrativa_tecnica" text,
    "narrativa_publica" text,
    "semeaduras" integer,
    "midia" character varying(2048),
    "outros_documentos_adicionais" character varying(2048),
    "numero_arvores_regenerando" integer,
    "descricao_da_regeneracao" text,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    "tm_sitio_id" integer,
    CONSTRAINT "tm_relatorio_sitio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_relatorio_sitio_uuid_key ON public.tm_relatorio_sitio USING btree (uuid);

CREATE UNIQUE INDEX tm_relatorio_sitio_uuid ON public.tm_relatorio_sitio USING btree (uuid);

CREATE INDEX tm_relatorio_sitio_tm_sitio_id ON public.tm_relatorio_sitio USING btree (tm_sitio_id);


CREATE SEQUENCE tm_relatorio_sitio_photos_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_relatorio_sitio_photos" (
    "id" integer DEFAULT nextval('tm_relatorio_sitio_photos_id_seq') NOT NULL,
    "relatorio_id" integer NOT NULL,
    "evidencia_id" integer NOT NULL,
    CONSTRAINT "tm_relatorio_sitio_photos_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX tm_relatorio_sitio_photos_relatorio_id ON public.tm_relatorio_sitio_photos USING btree (relatorio_id);

CREATE INDEX tm_relatorio_sitio_photos_evidencia_id ON public.tm_relatorio_sitio_photos USING btree (evidencia_id);


CREATE SEQUENCE tm_relatorio_sitio_tem_especie_arvore_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_relatorio_sitio_tem_especie_arvore" (
    "id" integer DEFAULT nextval('tm_relatorio_sitio_tem_especie_arvore_id_seq') NOT NULL,
    "relatorio_sitio_id" integer NOT NULL,
    "especie_id" integer NOT NULL,
    "quantidade" integer,
    CONSTRAINT "tm_relatorio_sitio_tem_especie_arvore_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


CREATE SEQUENCE tm_sitio_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_sitio" (
    "id" integer DEFAULT nextval('tm_sitio_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "projeto_id" integer NOT NULL,
    "nome" character varying(255),
    "link_terramatch" text,
    "status" character varying(50),
    "descricao" text,
    "historico" text,
    "data_inicio" date,
    "data_fim" date,
    "posse_categoria_id" integer,
    "taxa_sobrevivencia_plantada" integer,
    "meta_cobertura_cinco_anos" integer,
    "taxa_sobrevivencia_semeadura_direta" integer,
    "arvores_regeneracao_natural_por_hectare" integer,
    "regeneracao_natural_indice" numeric(10,2),
    "meta_numero_arvores_maduras" integer,
    "condicao_solo" text,
    "padrao_plantio" text,
    "estratos" text,
    "sementes" text,
    "arquivos_adicionais" text,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "tm_sitio_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_sitio_uuid_key ON public.tm_sitio USING btree (uuid);

CREATE UNIQUE INDEX tm_sitio_uuid ON public.tm_sitio USING btree (uuid);

CREATE INDEX tm_sitio_projeto_id ON public.tm_sitio USING btree (projeto_id);

CREATE INDEX tm_sitio_status ON public.tm_sitio USING btree (status);

CREATE INDEX tm_sitio_data_inicio ON public.tm_sitio USING btree (data_inicio);

CREATE INDEX tm_sitio_data_fim ON public.tm_sitio USING btree (data_fim);

CREATE INDEX tm_sitio_nome ON public.tm_sitio USING btree (nome);

CREATE INDEX tm_sitio_posse_categoria_id ON public.tm_sitio USING btree (posse_categoria_id);


CREATE SEQUENCE tm_sitio_tem_especie_arvore_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_sitio_tem_especie_arvore" (
    "id" integer DEFAULT nextval('tm_sitio_tem_especie_arvore_id_seq') NOT NULL,
    "tm_sitio_id" integer NOT NULL,
    "especie_id" integer NOT NULL,
    "invasora" boolean DEFAULT false,
    "observacao" text,
    CONSTRAINT "tm_sitio_tem_especie_arvore_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_sitio_tem_especie_arvore_tm_sitio_id_especie_id ON public.tm_sitio_tem_especie_arvore USING btree (tm_sitio_id, especie_id);


CREATE SEQUENCE tm_sitio_tem_especie_invasora_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_sitio_tem_especie_invasora" (
    "id" integer DEFAULT nextval('tm_sitio_tem_especie_invasora_id_seq') NOT NULL,
    "tm_sitio_id" integer NOT NULL,
    "especie_id" integer NOT NULL,
    "observacao" text,
    "criado_em" timestamptz NOT NULL,
    "atualizado_em" timestamptz NOT NULL,
    "deletado_em" timestamptz,
    CONSTRAINT "tm_sitio_tem_especie_invasora_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_sitio_tem_especie_invasora_tm_sitio_id_especie_id ON public.tm_sitio_tem_especie_invasora USING btree (tm_sitio_id, especie_id);


CREATE SEQUENCE tm_sitio_tem_tecnica_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_sitio_tem_tecnica" (
    "id" integer DEFAULT nextval('tm_sitio_tem_tecnica_id_seq') NOT NULL,
    "tm_sitio_id" integer NOT NULL,
    "tecnica_id" integer NOT NULL,
    "observacao" text,
    CONSTRAINT "tm_sitio_tem_tecnica_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_sitio_tem_tecnica_tm_sitio_id_tecnica_id ON public.tm_sitio_tem_tecnica USING btree (tm_sitio_id, tecnica_id);


CREATE SEQUENCE tm_sitio_tem_tipo_uso_solo_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."tm_sitio_tem_tipo_uso_solo" (
    "id" integer DEFAULT nextval('tm_sitio_tem_tipo_uso_solo_id_seq') NOT NULL,
    "tm_sitio_id" integer NOT NULL,
    "tipo_uso_solo_id" integer NOT NULL,
    "observacao" text,
    CONSTRAINT "tm_sitio_tem_tipo_uso_solo_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX tm_sitio_tem_tipo_uso_solo_tm_sitio_id_tipo_uso_solo_id ON public.tm_sitio_tem_tipo_uso_solo USING btree (tm_sitio_id, tipo_uso_solo_id);


CREATE SEQUENCE user_session_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."user_session" (
    "id" integer DEFAULT nextval('user_session_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "sid" character varying(255) NOT NULL,
    "user_uuid" uuid NOT NULL,
    "ip_address" character varying(255),
    "user_agent" character varying(255),
    "last_activity" timestamptz,
    "expires" timestamptz,
    "status" character varying(255) DEFAULT 'active' NOT NULL,
    "createdAt" timestamptz NOT NULL,
    CONSTRAINT "user_session_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX user_session_uuid_key ON public.user_session USING btree (uuid);

CREATE UNIQUE INDEX user_session_sid_key ON public.user_session USING btree (sid);


CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 2 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "name" character varying(255) NOT NULL,
    "email" character varying(255) NOT NULL,
    "password" character varying(255) NOT NULL,
    "profile_img" character varying(255),
    "role" enum_users_role DEFAULT 'user',
    "vterms" character varying(255),
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

COMMENT ON COLUMN "public"."users"."vterms" IS 'Versão dos termos de uso aceitos pelo usuário';

CREATE UNIQUE INDEX users_uuid_key ON public.users USING btree (uuid);

CREATE UNIQUE INDEX users_email_key ON public.users USING btree (email);


CREATE SEQUENCE vcode_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."vcode" (
    "id" integer DEFAULT nextval('vcode_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "email" character varying(255) NOT NULL,
    "codigo" character varying(6) NOT NULL,
    "tipo" enum_vcode_tipo NOT NULL,
    "usado_em" timestamptz,
    "expira_em" timestamptz NOT NULL,
    "tentativas" integer DEFAULT '0' NOT NULL,
    "createdAt" timestamptz NOT NULL,
    "updatedAt" timestamptz NOT NULL,
    "deletedAt" timestamptz,
    CONSTRAINT "vcode_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX vcode_uuid_key ON public.vcode USING btree (uuid);


CREATE SEQUENCE viveiro_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."viveiro" (
    "id" integer DEFAULT nextval('viveiro_id_seq') NOT NULL,
    "uuid" uuid NOT NULL,
    "nome" character varying(45),
    "descricao" character varying(100),
    "pessoa_id" integer NOT NULL,
    "localizacao_id" integer NOT NULL,
    "projeto_id" integer,
    CONSTRAINT "viveiro_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE UNIQUE INDEX viveiro_uuid_key ON public.viveiro USING btree (uuid);


CREATE SEQUENCE y0_database_arvore_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."y0_database_arvore" (
    "id" integer DEFAULT nextval('y0_database_arvore_id_seq') NOT NULL,
    "parcela_id" integer,
    "total_arvores_g_t_e10" integer DEFAULT '0' NOT NULL,
    "total_arvores_l_t10" integer DEFAULT '0' NOT NULL,
    "total_geral" integer DEFAULT '0' NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    CONSTRAINT "y0_database_arvore_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);


ALTER TABLE ONLY "public"."analise_relatorio" ADD CONSTRAINT "analise_relatorio_avaliado_por_id_fkey" FOREIGN KEY (avaliado_por_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."analise_relatorio" ADD CONSTRAINT "analise_relatorio_enviado_por_id_fkey" FOREIGN KEY (enviado_por_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."analise_relatorio" ADD CONSTRAINT "analise_relatorio_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."analise_relatorio" ADD CONSTRAINT "analise_relatorio_tm_relatorio_projeto_id_fkey" FOREIGN KEY (tm_relatorio_projeto_id) REFERENCES tm_relatorio_projeto(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."analise_relatorio" ADD CONSTRAINT "analise_relatorio_tm_relatorio_sitio_id_fkey" FOREIGN KEY (tm_relatorio_sitio_id) REFERENCES tm_relatorio_sitio(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."arvore" ADD CONSTRAINT "arvore_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."arvore" ADD CONSTRAINT "arvore_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE RESTRICT NOT DEFERRABLE;

ALTER TABLE ONLY "public"."arvore_plantada_dap_10cm" ADD CONSTRAINT "arvore_plantada_dap_10cm_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."arvore_plantada_dap_10cm" ADD CONSTRAINT "arvore_plantada_dap_10cm_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."atividade" ADD CONSTRAINT "atividade_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."banco" ADD CONSTRAINT "banco_banco_id_fkey" FOREIGN KEY (banco_id) REFERENCES estrato(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."banco" ADD CONSTRAINT "banco_estrato_id_fkey" FOREIGN KEY (estrato_id) REFERENCES estrato(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."banco" ADD CONSTRAINT "banco_poligono_id_fkey" FOREIGN KEY (poligono_id) REFERENCES poligono(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."banco" ADD CONSTRAINT "banco_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."banco" ADD CONSTRAINT "banco_sitio_id_fkey" FOREIGN KEY (sitio_id) REFERENCES sitio(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."banco" ADD CONSTRAINT "banco_tecnica_id_fkey" FOREIGN KEY (tecnica_id) REFERENCES tecnica(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."convite" ADD CONSTRAINT "convite_vcode_fkey" FOREIGN KEY (vcode) REFERENCES vcode(uuid) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."coordenadas_pacto" ADD CONSTRAINT "coordenadas_pacto_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."coordenadas_ppc" ADD CONSTRAINT "coordenadas_ppc_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."demografia_dos_dias_uteis_has_etnia" ADD CONSTRAINT "demografia_dos_dias_uteis_ha_demografia_dos_dias_uteis_id_fkey2" FOREIGN KEY (demografia_dos_dias_uteis_id) REFERENCES demografia_dos_dias_uteis(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."demografia_dos_dias_uteis_has_etnia" ADD CONSTRAINT "demografia_dos_dias_uteis_has_etnia_etnia_id_fkey" FOREIGN KEY (etnia_id) REFERENCES etnia(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."demografia_dos_dias_uteis_has_faixa_etaria" ADD CONSTRAINT "demografia_dos_dias_uteis_ha_demografia_dos_dias_uteis_id_fkey1" FOREIGN KEY (demografia_dos_dias_uteis_id) REFERENCES demografia_dos_dias_uteis(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."demografia_dos_dias_uteis_has_faixa_etaria" ADD CONSTRAINT "demografia_dos_dias_uteis_has_faixa_etaria_faixa_etaria_id_fkey" FOREIGN KEY (faixa_etaria_id) REFERENCES faixa_etaria(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."demografia_dos_dias_uteis_has_genero" ADD CONSTRAINT "demografia_dos_dias_uteis_has_demografia_dos_dias_uteis_id_fkey" FOREIGN KEY (demografia_dos_dias_uteis_id) REFERENCES demografia_dos_dias_uteis(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."demografia_dos_dias_uteis_has_genero" ADD CONSTRAINT "demografia_dos_dias_uteis_has_genero_genero_id_fkey" FOREIGN KEY (genero_id) REFERENCES genero(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."diagnostico" ADD CONSTRAINT "diagnostico_implantacao_id_fkey" FOREIGN KEY (implantacao_id) REFERENCES implantacao(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."docs_imovel_rural" ADD CONSTRAINT "docs_imovel_rural_imovel_rural_id_fkey" FOREIGN KEY (imovel_rural_id) REFERENCES imovel_rural(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."evidencia" ADD CONSTRAINT "evidencia_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."imovel_rural" ADD CONSTRAINT "imovel_rural_categoria_id_fkey" FOREIGN KEY (categoria_id) REFERENCES categoria(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."imovel_rural" ADD CONSTRAINT "imovel_rural_criado_por_fkey" FOREIGN KEY (criado_por) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."imovel_rural" ADD CONSTRAINT "imovel_rural_localizacao_id_fkey" FOREIGN KEY (localizacao_id) REFERENCES localizacao(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."implantacao" ADD CONSTRAINT "implantacao_banco_id_fkey" FOREIGN KEY (banco_id) REFERENCES banco(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."implantacao" ADD CONSTRAINT "implantacao_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."item_implantacao" ADD CONSTRAINT "item_implantacao_implantacao_id_fkey" FOREIGN KEY (implantacao_id) REFERENCES implantacao(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."item_implantacao" ADD CONSTRAINT "item_implantacao_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."item_manutencao" ADD CONSTRAINT "item_manutencao_implantacao_id_fkey" FOREIGN KEY (implantacao_id) REFERENCES implantacao(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."item_manutencao" ADD CONSTRAINT "item_manutencao_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."item_monitoramento" ADD CONSTRAINT "item_monitoramento_implantacao_id_fkey" FOREIGN KEY (implantacao_id) REFERENCES implantacao(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."item_monitoramento" ADD CONSTRAINT "item_monitoramento_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."localizacao" ADD CONSTRAINT "localizacao_municipio_id_fkey" FOREIGN KEY (municipio_id) REFERENCES municipio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."matricula" ADD CONSTRAINT "matricula_imovel_rural_id_fkey" FOREIGN KEY (imovel_rural_id) REFERENCES imovel_rural(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."membros" ADD CONSTRAINT "membros_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."membros" ADD CONSTRAINT "membros_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."midia_adicional_parcela" ADD CONSTRAINT "midia_adicional_parcela_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."monitoramento" ADD CONSTRAINT "monitoramento_organizacao_id_fkey" FOREIGN KEY (organizacao_id) REFERENCES pessoa(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."monitoramento" ADD CONSTRAINT "monitoramento_responsavel_coleta_id_fkey" FOREIGN KEY (responsavel_coleta_id) REFERENCES pessoa(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."monitoramento" ADD CONSTRAINT "monitoramento_submitted_by_id_fkey" FOREIGN KEY (submitted_by_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."muda" ADD CONSTRAINT "muda_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."muda" ADD CONSTRAINT "muda_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES relatorio(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."muda" ADD CONSTRAINT "muda_viveiro_id_fkey" FOREIGN KEY (viveiro_id) REFERENCES viveiro(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."municipio" ADD CONSTRAINT "municipio_estado_id_fkey" FOREIGN KEY (estado_id) REFERENCES estado(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."parcela_monitoramento" ADD CONSTRAINT "parcela_monitoramento_monitoramento_id_fkey" FOREIGN KEY (monitoramento_id) REFERENCES monitoramento(id) ON UPDATE CASCADE ON DELETE RESTRICT NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pessoa" ADD CONSTRAINT "pessoa_usuario_id_fkey" FOREIGN KEY (usuario_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pessoa_fisica" ADD CONSTRAINT "pessoa_fisica_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pessoa_juridica" ADD CONSTRAINT "pessoa_juridica_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pessoa_tem_email" ADD CONSTRAINT "pessoa_tem_email_email_id_fkey" FOREIGN KEY (email_id) REFERENCES email(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."pessoa_tem_email" ADD CONSTRAINT "pessoa_tem_email_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."pessoa_tem_telefone" ADD CONSTRAINT "pessoa_tem_telefone_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."pessoa_tem_telefone" ADD CONSTRAINT "pessoa_tem_telefone_telefone_id_fkey" FOREIGN KEY (telefone_id) REFERENCES telefone(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."poligono" ADD CONSTRAINT "poligono_sitio_id_fkey" FOREIGN KEY (sitio_id) REFERENCES sitio(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."projeto" ADD CONSTRAINT "projeto_criado_por_fkey" FOREIGN KEY (criado_por) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."projeto_tem_especie_planta" ADD CONSTRAINT "projeto_tem_especie_planta_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."projeto_tem_especie_planta" ADD CONSTRAINT "projeto_tem_especie_planta_manejo_id_fkey" FOREIGN KEY (manejo_id) REFERENCES manejo(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."projeto_tem_especie_planta" ADD CONSTRAINT "projeto_tem_especie_planta_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."projeto_tem_imovel" ADD CONSTRAINT "projeto_tem_imovel_imovel_rural_id_fkey" FOREIGN KEY (imovel_rural_id) REFERENCES imovel_rural(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."projeto_tem_imovel" ADD CONSTRAINT "projeto_tem_imovel_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."projeto_tem_metodologia" ADD CONSTRAINT "projeto_tem_metodologia_metodologia_id_fkey" FOREIGN KEY (metodologia_id) REFERENCES metodologia(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."projeto_tem_metodologia" ADD CONSTRAINT "projeto_tem_metodologia_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."relatorio" ADD CONSTRAINT "relatorio_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."relatorio_projeto_has_demografia_dos_dias_uteis" ADD CONSTRAINT "relatorio_projeto_has_demogra_demografia_dos_dias_uteis_id_fkey" FOREIGN KEY (demografia_dos_dias_uteis_id) REFERENCES demografia_dos_dias_uteis(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."relatorio_projeto_has_demografia_dos_dias_uteis" ADD CONSTRAINT "relatorio_projeto_has_demografia_dos__relatorio_projeto_id_fkey" FOREIGN KEY (relatorio_projeto_id) REFERENCES tm_relatorio_projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."relatorio_sitio_has_demografia_dos_dias_uteis" ADD CONSTRAINT "relatorio_sitio_has_demografi_demografia_dos_dias_uteis_id_fkey" FOREIGN KEY (demografia_dos_dias_uteis_id) REFERENCES demografia_dos_dias_uteis(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."relatorio_sitio_has_demografia_dos_dias_uteis" ADD CONSTRAINT "relatorio_sitio_has_demografia_dos_dias_relatorio_sitio_id_fkey" FOREIGN KEY (relatorio_sitio_id) REFERENCES tm_relatorio_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."responsavel_imovel" ADD CONSTRAINT "responsavel_imovel_imovel_rural_id_fkey" FOREIGN KEY (imovel_rural_id) REFERENCES imovel_rural(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."responsavel_imovel" ADD CONSTRAINT "responsavel_imovel_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."semente" ADD CONSTRAINT "semente_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."sitio" ADD CONSTRAINT "sitio_imovel_rural_id_fkey" FOREIGN KEY (imovel_rural_id) REFERENCES imovel_rural(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."subparcela_arvore" ADD CONSTRAINT "subparcela_arvore_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."subparcela_arvore" ADD CONSTRAINT "subparcela_arvore_subparcela_id_fkey" FOREIGN KEY (subparcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."subparcela_monitoramento" ADD CONSTRAINT "subparcela_monitoramento_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE RESTRICT NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tecnica" ADD CONSTRAINT "tecnica_metodologia_id_fkey" FOREIGN KEY (metodologia_id) REFERENCES metodologia(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."terms_of_use" ADD CONSTRAINT "terms_of_use_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_disturbio" ADD CONSTRAINT "tm_disturbio_relatorio_sitio_id_fkey" FOREIGN KEY (relatorio_sitio_id) REFERENCES tm_relatorio_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_geometria_sitio" ADD CONSTRAINT "tm_geometria_sitio_tm_sitio_id_fkey" FOREIGN KEY (tm_sitio_id) REFERENCES tm_sitio(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_membro_projeto" ADD CONSTRAINT "tm_membro_projeto_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_membro_projeto" ADD CONSTRAINT "tm_membro_projeto_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_projeto" ADD CONSTRAINT "tm_projeto_criado_por_fkey" FOREIGN KEY (criado_por) REFERENCES users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_projeto_tem_especie_arvore" ADD CONSTRAINT "tm_projeto_tem_especie_arvore_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_projeto_tem_especie_arvore" ADD CONSTRAINT "tm_projeto_tem_especie_arvore_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_projeto_tem_especie_arvore" ADD CONSTRAINT "tm_projeto_tem_especie_arvore_tm_projeto_id_fkey" FOREIGN KEY (tm_projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_projeto_tem_tecnica" ADD CONSTRAINT "tm_projeto_tem_tecnica_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_projeto_tem_tecnica" ADD CONSTRAINT "tm_projeto_tem_tecnica_tecnica_id_fkey" FOREIGN KEY (tecnica_id) REFERENCES tecnica(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_projeto_tem_tecnica" ADD CONSTRAINT "tm_projeto_tem_tecnica_tm_projeto_id_fkey" FOREIGN KEY (tm_projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_projeto_tem_tipo_uso_solo" ADD CONSTRAINT "tm_projeto_tem_tipo_uso_solo_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_projeto_tem_tipo_uso_solo" ADD CONSTRAINT "tm_projeto_tem_tipo_uso_solo_tipo_uso_solo_id_fkey" FOREIGN KEY (tipo_uso_solo_id) REFERENCES tipo_uso_solo(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_projeto_tem_tipo_uso_solo" ADD CONSTRAINT "tm_projeto_tem_tipo_uso_solo_tm_projeto_id_fkey" FOREIGN KEY (tm_projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_relatorio_projeto" ADD CONSTRAINT "tm_relatorio_projeto_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_relatorio_projeto_photos" ADD CONSTRAINT "tm_relatorio_projeto_photos_evidencia_id_fkey" FOREIGN KEY (evidencia_id) REFERENCES tm_evidencias_e_registro_fotografico(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_relatorio_projeto_photos" ADD CONSTRAINT "tm_relatorio_projeto_photos_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES tm_relatorio_projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_relatorio_sitio" ADD CONSTRAINT "tm_relatorio_sitio_tm_sitio_id_fkey" FOREIGN KEY (tm_sitio_id) REFERENCES tm_sitio(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_relatorio_sitio_photos" ADD CONSTRAINT "tm_relatorio_sitio_photos_evidencia_id_fkey" FOREIGN KEY (evidencia_id) REFERENCES tm_evidencias_e_registro_fotografico(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_relatorio_sitio_photos" ADD CONSTRAINT "tm_relatorio_sitio_photos_relatorio_id_fkey" FOREIGN KEY (relatorio_id) REFERENCES tm_relatorio_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_relatorio_sitio_tem_especie_arvore" ADD CONSTRAINT "tm_relatorio_sitio_tem_especie_arvore_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_relatorio_sitio_tem_especie_arvore" ADD CONSTRAINT "tm_relatorio_sitio_tem_especie_arvore_relatorio_sitio_id_fkey" FOREIGN KEY (relatorio_sitio_id) REFERENCES tm_relatorio_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_sitio" ADD CONSTRAINT "tm_sitio_posse_categoria_id_fkey" FOREIGN KEY (posse_categoria_id) REFERENCES categoria(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_sitio" ADD CONSTRAINT "tm_sitio_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES tm_projeto(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_sitio_tem_especie_arvore" ADD CONSTRAINT "tm_sitio_tem_especie_arvore_especie_id_fkey" FOREIGN KEY (especie_id) REFERENCES especie(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_sitio_tem_especie_arvore" ADD CONSTRAINT "tm_sitio_tem_especie_arvore_tm_sitio_id_fkey" FOREIGN KEY (tm_sitio_id) REFERENCES tm_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_sitio_tem_tecnica" ADD CONSTRAINT "tm_sitio_tem_tecnica_tecnica_id_fkey" FOREIGN KEY (tecnica_id) REFERENCES tecnica(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_sitio_tem_tecnica" ADD CONSTRAINT "tm_sitio_tem_tecnica_tm_sitio_id_fkey" FOREIGN KEY (tm_sitio_id) REFERENCES tm_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."tm_sitio_tem_tipo_uso_solo" ADD CONSTRAINT "tm_sitio_tem_tipo_uso_solo_tipo_uso_solo_id_fkey" FOREIGN KEY (tipo_uso_solo_id) REFERENCES tipo_uso_solo(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."tm_sitio_tem_tipo_uso_solo" ADD CONSTRAINT "tm_sitio_tem_tipo_uso_solo_tm_sitio_id_fkey" FOREIGN KEY (tm_sitio_id) REFERENCES tm_sitio(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."viveiro" ADD CONSTRAINT "viveiro_localizacao_id_fkey" FOREIGN KEY (localizacao_id) REFERENCES localizacao(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."viveiro" ADD CONSTRAINT "viveiro_pessoa_id_fkey" FOREIGN KEY (pessoa_id) REFERENCES pessoa(id) ON UPDATE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."viveiro" ADD CONSTRAINT "viveiro_projeto_id_fkey" FOREIGN KEY (projeto_id) REFERENCES projeto(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."y0_database_arvore" ADD CONSTRAINT "y0_database_arvore_parcela_id_fkey" FOREIGN KEY (parcela_id) REFERENCES parcela_monitoramento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

DROP TABLE IF EXISTS "geography_columns";
CREATE VIEW "geography_columns" AS SELECT current_database() AS f_table_catalog,
    n.nspname AS f_table_schema,
    c.relname AS f_table_name,
    a.attname AS f_geography_column,
    postgis_typmod_dims(a.atttypmod) AS coord_dimension,
    postgis_typmod_srid(a.atttypmod) AS srid,
    postgis_typmod_type(a.atttypmod) AS type
   FROM pg_class c,
    pg_attribute a,
    pg_type t,
    pg_namespace n
  WHERE ((t.typname = 'geography'::name) AND (a.attisdropped = false) AND (a.atttypid = t.oid) AND (a.attrelid = c.oid) AND (c.relnamespace = n.oid) AND (c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND (NOT pg_is_other_temp_schema(c.relnamespace)) AND has_table_privilege(c.oid, 'SELECT'::text));

DROP TABLE IF EXISTS "geometry_columns";
CREATE VIEW "geometry_columns" AS SELECT (current_database())::character varying(256) AS f_table_catalog,
    n.nspname AS f_table_schema,
    c.relname AS f_table_name,
    a.attname AS f_geometry_column,
    COALESCE(postgis_typmod_dims(a.atttypmod), sn.ndims, 2) AS coord_dimension,
    COALESCE(NULLIF(postgis_typmod_srid(a.atttypmod), 0), sr.srid, 0) AS srid,
    (replace(replace(COALESCE(NULLIF(upper(postgis_typmod_type(a.atttypmod)), 'GEOMETRY'::text), st.type, 'GEOMETRY'::text), 'ZM'::text, ''::text), 'Z'::text, ''::text))::character varying(30) AS type
   FROM ((((((pg_class c
     JOIN pg_attribute a ON (((a.attrelid = c.oid) AND (NOT a.attisdropped))))
     JOIN pg_namespace n ON ((c.relnamespace = n.oid)))
     JOIN pg_type t ON ((a.atttypid = t.oid)))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            replace(split_part(s.consrc, ''''::text, 2), ')'::text, ''::text) AS type
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE (s.consrc ~~* '%geometrytype(% = %'::text)) st ON (((st.connamespace = n.oid) AND (st.conrelid = c.oid) AND (a.attnum = ANY (st.conkey)))))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            (replace(split_part(s.consrc, ' = '::text, 2), ')'::text, ''::text))::integer AS ndims
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE (s.consrc ~~* '%ndims(% = %'::text)) sn ON (((sn.connamespace = n.oid) AND (sn.conrelid = c.oid) AND (a.attnum = ANY (sn.conkey)))))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            (replace(replace(split_part(s.consrc, ' = '::text, 2), ')'::text, ''::text), '('::text, ''::text))::integer AS srid
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE (s.consrc ~~* '%srid(% = %'::text)) sr ON (((sr.connamespace = n.oid) AND (sr.conrelid = c.oid) AND (a.attnum = ANY (sr.conkey)))))
  WHERE ((c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND (NOT (c.relname = 'raster_columns'::name)) AND (t.typname = 'geometry'::name) AND (NOT pg_is_other_temp_schema(c.relnamespace)) AND has_table_privilege(c.oid, 'SELECT'::text));

-- 2025-09-23 17:13:39 UTC
