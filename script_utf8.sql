USE [master]
GO
/****** Object:  Database [qr_assist]    Script Date: 22/06/2026 20:32:11 ******/
CREATE DATABASE [qr_assist]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'qr_assist', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\qr_assist.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'qr_assist_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\qr_assist_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [qr_assist] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [qr_assist].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [qr_assist] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [qr_assist] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [qr_assist] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [qr_assist] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [qr_assist] SET ARITHABORT OFF 
GO
ALTER DATABASE [qr_assist] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [qr_assist] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [qr_assist] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [qr_assist] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [qr_assist] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [qr_assist] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [qr_assist] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [qr_assist] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [qr_assist] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [qr_assist] SET  DISABLE_BROKER 
GO
ALTER DATABASE [qr_assist] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [qr_assist] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [qr_assist] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [qr_assist] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [qr_assist] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [qr_assist] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [qr_assist] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [qr_assist] SET RECOVERY FULL 
GO
ALTER DATABASE [qr_assist] SET  MULTI_USER 
GO
ALTER DATABASE [qr_assist] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [qr_assist] SET DB_CHAINING OFF 
GO
ALTER DATABASE [qr_assist] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [qr_assist] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [qr_assist] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [qr_assist] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'qr_assist', N'ON'
GO
ALTER DATABASE [qr_assist] SET QUERY_STORE = ON
GO
ALTER DATABASE [qr_assist] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [qr_assist]
GO
/****** Object:  User [proyecto_grado]    Script Date: 22/06/2026 20:32:11 ******/
CREATE USER [proyecto_grado] FOR LOGIN [proyecto_grado] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_owner] ADD MEMBER [proyecto_grado]
GO
/****** Object:  Table [dbo].[Asistencia]    Script Date: 22/06/2026 20:32:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Asistencia](
	[ID_Asistencia] [int] IDENTITY(1,1) NOT NULL,
	[ID_Empleado] [int] NOT NULL,
	[Fecha] [date] NOT NULL,
	[Hora_entrada] [time](7) NOT NULL,
	[Estado] [varchar](20) NOT NULL,
 CONSTRAINT [PK_Asistencia] PRIMARY KEY CLUSTERED 
(
	[ID_Asistencia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Empleados]    Script Date: 22/06/2026 20:32:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Empleados](
	[ID_Empleado] [int] IDENTITY(1,1) NOT NULL,
	[Nombres] [varchar](20) NOT NULL,
	[Apellidos] [varchar](20) NOT NULL,
	[Cargo] [varchar](25) NOT NULL,
	[Codigo_qr] [varchar](255) NULL,
	[Estado] [varchar](10) NOT NULL,
 CONSTRAINT [PK_Empleados] PRIMARY KEY CLUSTERED 
(
	[ID_Empleado] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Usuarios]    Script Date: 22/06/2026 20:32:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Usuarios](
	[ID_Usuario] [int] IDENTITY(1,1) NOT NULL,
	[ID_Empleado] [int] NULL,
	[Nombres] [varchar](20) NULL,
	[Apellidos] [varchar](20) NULL,
	[Username] [varchar](20) NOT NULL,
	[Contraseña] [varchar](30) NOT NULL,
	[Rol] [varchar](20) NOT NULL,
 CONSTRAINT [PK__Usuarios__DE4431C5A965811B] PRIMARY KEY CLUSTERED 
(
	[ID_Usuario] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[Asistencia] ON 

INSERT [dbo].[Asistencia] ([ID_Asistencia], [ID_Empleado], [Fecha], [Hora_entrada], [Estado]) VALUES (1, 1, CAST(N'2026-06-12' AS Date), CAST(N'15:16:28.8600000' AS Time), N'Tarde')
INSERT [dbo].[Asistencia] ([ID_Asistencia], [ID_Empleado], [Fecha], [Hora_entrada], [Estado]) VALUES (2, 1, CAST(N'2026-06-16' AS Date), CAST(N'14:20:23.8300000' AS Time), N'Tarde')
SET IDENTITY_INSERT [dbo].[Asistencia] OFF
GO
SET IDENTITY_INSERT [dbo].[Empleados] ON 

INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (1, N'Juan Emilio', N'Perez Ramirez', N'Gerente', N'7WTOD9E3GIW62LJ0', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (2, N'Marta Antonia', N'Jimenez Nolasco', N'Subgerente', N'9YT1O07WC1G74SFY', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (3, N'Antonieta', N'Gomez Sanchez', N'Encargado', N'NEUMFKW0ZJOP1NEI', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (4, N'Aurora Ximena', N'Batista Barrera', N'Asistente', N'0W8M5G5J648JN1L3', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (5, N'Annys Teresa', N'Rodriguez Alcantara', N'Asistente', N'96K5QUWOLEZCW0OD', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (6, N'Gregorio Gerundio', N'Felix Martinez', N'Analista', N'P2KU6E4Z5SUJYUI6', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (7, N'Julieta Mariel', N'Appoloni Castro', N'Director', N'YOX92TUPEUR7OOYL', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (8, N'Jose Manuel', N'Cuevas Mancebo', N'Subgerente', N'W1L666T37UOHWAW6', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (9, N'Martin Julio', N'Hernandez Reina', N'Analista Junior', N'ZM5WYZK98URRPN1F', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (10, N'Ana Katherine', N'Selmo Lopez', N'Encargado', N'NEZLTOOKRYP39EER', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (11, N'Carlos Manuel', N'De los Santos Cruz', N'Supervisor', N'ZJUY1GLH1EEAJVR0', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (12, N'Altagracia', N'Rosario Valdez', N'Coordinador', N'F1FU2UHD4PS4PH5P', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (13, N'Yuleisy', N'Polanco Marte', N'Recepcionista', N'MRWROT6XL5DREMYZ', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (14, N'Braulio Alberto', N'Grullon Mejia', N'Auditor', N'EL9MD5M2LAK0PZN0', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (15, N'Dahiana Nicole', N'Suero Peguero', N'Pasante', N'CKGOUVBL2COLE17J', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (16, N'Wander Jose ', N'Franco Tavares', N'Tecnico', N'PJJ3QIFB1215O9X0', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (17, N'Soraya Esther', N'Disla Matos', N'Consultor', N'0569NXGDB7UDHF7M', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (18, N'Franklin Eduardo', N'Pichardo Abreu', N'Pasante', N'A697SEELT7QPU6GS', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (19, N'Milagros del Carmen', N'De la Rosa Paulino', N'Gerente', N'4K1VA9WRUX1CFCX6', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (20, N'Starling Javier', N'Minaya Veras', N'Analista Senior', N'T2EF9W681JNCLM7Z', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (21, N'Raysa Maria ', N'Peralta Cordero', N'Asistente', N'7DC2SVHGFYH6U6BA', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (22, N'Diomedes Antonio', N'Lora Espinal', N'Encargado ', N'TL5P7GEC93P9NZZT', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (23, N'Xiomara Altagracia', N'Ureña Collado', N'Contador', N'AJ4YPH29IWS6IM66', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (24, N'Kelvin Francisco', N'Fermin Sosa', N'Soporte Tecnico', N'JV30IAJZB6KPK59K', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (25, N'Esmeralda ', N'Amarante Cruz', N'Secretaria', N'OFHI7R447P3KJL4C', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (51, N'Olandis Junior', N'Batista Cuevas', N'TI', N'TTTQT04MCAX277PC', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (52, N'Matirelys', N'Alcantara', N'TI', N'OJCTZ9KJY2IW9MRD', N'Activo')
INSERT [dbo].[Empleados] ([ID_Empleado], [Nombres], [Apellidos], [Cargo], [Codigo_qr], [Estado]) VALUES (53, N'Miguel', N'Zabala', N'TI', N'LIM3ZEM1F72E9V09', N'Activo')
SET IDENTITY_INSERT [dbo].[Empleados] OFF
GO
SET IDENTITY_INSERT [dbo].[Usuarios] ON 

INSERT [dbo].[Usuarios] ([ID_Usuario], [ID_Empleado], [Nombres], [Apellidos], [Username], [Contraseña], [Rol]) VALUES (5, 51, N'Olandis Junior', N'Batista Cuevas', N'JUNIOR', N'1234', N'Administrador')
INSERT [dbo].[Usuarios] ([ID_Usuario], [ID_Empleado], [Nombres], [Apellidos], [Username], [Contraseña], [Rol]) VALUES (6, 52, N'Matirelys', N'Alcantara', N'MATIRELYS', N'1234', N'Administrador')
INSERT [dbo].[Usuarios] ([ID_Usuario], [ID_Empleado], [Nombres], [Apellidos], [Username], [Contraseña], [Rol]) VALUES (7, 53, N'Miguel', N'Zabala', N'ZABALA', N'polonia', N'Administrador')
INSERT [dbo].[Usuarios] ([ID_Usuario], [ID_Empleado], [Nombres], [Apellidos], [Username], [Contraseña], [Rol]) VALUES (9, 1, N'Juan Emilio', N'Perez Ramirez', N'JUAN', N'123', N'Empleado')
SET IDENTITY_INSERT [dbo].[Usuarios] OFF
GO
/****** Object:  Index [IX_Empleados]    Script Date: 22/06/2026 20:32:12 ******/
CREATE UNIQUE NONCLUSTERED INDEX [IX_Empleados] ON [dbo].[Empleados]
(
	[ID_Empleado] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Asistencia]  WITH CHECK ADD  CONSTRAINT [FK_ID_Empleado] FOREIGN KEY([ID_Empleado])
REFERENCES [dbo].[Empleados] ([ID_Empleado])
GO
ALTER TABLE [dbo].[Asistencia] CHECK CONSTRAINT [FK_ID_Empleado]
GO
ALTER TABLE [dbo].[Usuarios]  WITH CHECK ADD  CONSTRAINT [FK_Usuarios_Empleados] FOREIGN KEY([ID_Empleado])
REFERENCES [dbo].[Empleados] ([ID_Empleado])
GO
ALTER TABLE [dbo].[Usuarios] CHECK CONSTRAINT [FK_Usuarios_Empleados]
GO
/****** Object:  StoredProcedure [dbo].[Actualiza_Asistencia]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[Actualiza_Asistencia]
@id_asistencia int,
@id_empleado int,
@fecha date,
@hora_entrada time(7),
@estado varchar(20)

AS
BEGIN

update Asistencia
set ID_Empleado = @id_empleado,
	Fecha = @fecha,
	Hora_entrada = @hora_entrada,
	Estado = @estado

where ID_Asistencia = @id_asistencia

end
GO
/****** Object:  StoredProcedure [dbo].[Actualiza_Empleado]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[Actualiza_Empleado]
@id_empleado int,
@nombre varchar(20),
@apellido varchar(20),
@cargo varchar(15),
@codigo varchar(255),
@estado varchar(10)

AS
BEGIN

update Empleados
set Nombres = @nombre,
	Apellidos = @apellido,
	Cargo = @cargo,
	Codigo_qr = @codigo,
	Estado = @estado

where ID_Empleado = @id_empleado

end
GO
/****** Object:  StoredProcedure [dbo].[Actualiza_Usuario]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[Actualiza_Usuario]
@id_usuario int,
@idempleado int,
@nombres varchar(20),
@apellidos varchar(20),
@username varchar(20),
@contrasena varchar(30),
@rol varchar(20)

AS
BEGIN

update Usuarios
set ID_Empleado = @idempleado,
	Nombres = @nombres,
	Apellidos = @apellidos,
	username = @username,
	Contraseña = @contrasena,
	Rol = @rol

where ID_Usuario = @id_usuario

end
GO
/****** Object:  StoredProcedure [dbo].[Elimina_Asistencia]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[Elimina_Asistencia]
@id_asistencia int

AS
BEGIN

delete from Asistencia
where ID_Asistencia = @id_asistencia

end
GO
/****** Object:  StoredProcedure [dbo].[Elimina_Empleado]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[Elimina_Empleado]
@id_empleado int

AS
BEGIN

delete from Empleados
where ID_Empleado = @id_empleado

end
GO
/****** Object:  StoredProcedure [dbo].[Elimina_Usuario]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[Elimina_Usuario]
@id_usuario int

AS
BEGIN

delete from Usuarios
where ID_Usuario = @id_usuario

end
GO
/****** Object:  StoredProcedure [dbo].[Inserta_Asistencia]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[Inserta_Asistencia]
@id_empleado int,
@fecha date,
@entrada time(7),
@estado varchar(20)

AS
BEGIN

Insert INTO Asistencia(ID_Empleado, Fecha, Hora_entrada, estado)
VALUES(@id_empleado, @fecha, @entrada, @estado)

end
GO
/****** Object:  StoredProcedure [dbo].[Inserta_Empleado]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[Inserta_Empleado]
@nombre varchar(20),
@apellido varchar(20),
@cargo varchar(15),
@codigo varchar(255),
@estado varchar(10)

AS
BEGIN

Insert INTO Empleados(Nombres, Apellidos, Cargo, Codigo_qr, Estado)
VALUES(@nombre, @apellido, @cargo, @codigo, @estado)

end
GO
/****** Object:  StoredProcedure [dbo].[Inserta_Usuario]    Script Date: 22/06/2026 20:32:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[Inserta_Usuario]
@idempleado int,
@nombres varchar(20),
@apellidos varchar(20),
@username varchar(20),
@contrasena varchar(30),
@rol varchar(20)

AS
BEGIN

Insert INTO Usuarios(ID_Empleado, Nombres, Apellidos, Username, Contraseña, Rol)
VALUES(@idempleado, @nombres, @apellidos, @username, @contrasena, @rol)

end
GO
USE [master]
GO
ALTER DATABASE [qr_assist] SET  READ_WRITE 
GO
