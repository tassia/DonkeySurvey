-- phpMyAdmin SQL Dump
-- version 3.2.1deb1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tempo de Geração: Out 02, 2009 as 12:40 PM
-- Versão do Servidor: 5.1.37
-- Versão do PHP: 5.2.10-2.2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Banco de Dados: `donkeystats`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `file`
--

CREATE TABLE IF NOT EXISTS `file` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `hash` varchar(100) NOT NULL,
  `size` int(14) NOT NULL,
  `partial_size` int(14) NOT NULL,
  `best_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `file`
--


-- --------------------------------------------------------

--
-- Estrutura da tabela `filename`
--

CREATE TABLE IF NOT EXISTS `filename` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Filenames' AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `filename`
--


-- --------------------------------------------------------

--
-- Estrutura da tabela `file_filename`
--

CREATE TABLE IF NOT EXISTS `file_filename` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_file` int(11) NOT NULL,
  `id_filename` int(11) NOT NULL,
  UNIQUE KEY `id` (`id`),
  FOREIGN KEY (`id_file`) REFERENCES file(`id`),
  FOREIGN KEY (`id_filename`) REFERENCES filename(`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='One file can be identified by numerous filenames' AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `file_filename`
--


-- --------------------------------------------------------

--
-- Estrutura da tabela `session`
--

CREATE TABLE IF NOT EXISTS `session` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `client_id` varchar(50) NOT NULL,
  `client_name` varchar(50) NOT NULL,
  `client_ip` varchar(15) NOT NULL,
  `client_port` int(4) NOT NULL,
  `client_software` varchar(30) NOT NULL,
  `client_so` varchar(30) NOT NULL,
  `server_ip` datetime NOT NULL,
  `server_port` int(4) NOT NULL,
  `start_date` datetime NOT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COMMENT='Keep sessions information' AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `session`
--


-- --------------------------------------------------------

--
-- Estrutura da tabela `session_file`
--

CREATE TABLE IF NOT EXISTS `session_file` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_session` int(11) NOT NULL,
  `id_file` int(11) NOT NULL,
  `uploading` tinyint(1) NOT NULL,
  `downloading` tinyint(1) NOT NULL,
  FOREIGN KEY (`id_file`) REFERENCES file(`id`),
  FOREIGN KEY (`id_session`) REFERENCES session(`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `session_file`
--


-- --------------------------------------------------------

--
-- Estrutura da tabela `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `hash` varchar(100) NOT NULL,
  `total_downloaded` int(8) NOT NULL,
  `total_uploaded` int(8) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `user`
--


-- --------------------------------------------------------

--
-- Estrutura da tabela `user_file`
--

CREATE TABLE IF NOT EXISTS `user_file` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `id_user` int(11) NOT NULL,
  `id_file` int(11) NOT NULL,
  FOREIGN KEY (`id_user`) REFERENCES user(`id`),
  FOREIGN KEY (`id_file`) REFERENCES file(`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

--
-- Extraindo dados da tabela `user_file`
--


