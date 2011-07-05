SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

--CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;

USE `donkeystats`;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`address_has_file` (
  `address_id` BIGINT(20) UNSIGNED NOT NULL ,
  `file_id` BIGINT(20) UNSIGNED NOT NULL ,
  `first_seen` DATETIME NOT NULL ,
  PRIMARY KEY (`address_id`, `file_id`) ,
  INDEX `fk_address_has_file_address1` (`address_id` ASC) ,
  INDEX `fk_address_has_file_file1` (`file_id` ASC) ,
  CONSTRAINT `fk_address_has_file_address1`
    FOREIGN KEY (`address_id` )
    REFERENCES `donkeystats`.`address` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_address_has_file_file1`
    FOREIGN KEY (`file_id` )
    REFERENCES `donkeystats`.`file` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM 
DEFAULT CHARACTER SET = latin1
COLLATE = latin1_swedish_ci;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`address` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `ip` VARCHAR(45) NOT NULL ,
  `port` INT(11) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM 
DEFAULT CHARACTER SET = latin1
COLLATE = latin1_swedish_ci;

ALTER TABLE `donkeystats`.`source` CHANGE COLUMN `hash` `hash` VARCHAR(512) NOT NULL  , CHANGE COLUMN `availability` `availability` DECIMAL(2,1) NULL  ;

ALTER TABLE `donkeystats`.`session` DROP COLUMN `ip` , DROP COLUMN `port` , ADD COLUMN `address_id` BIGINT(20) UNSIGNED NOT NULL  AFTER `source_id` , ADD COLUMN `kind` VARCHAR(45) NULL DEFAULT NULL  AFTER `address_id` , CHANGE COLUMN `uploaded` `uploaded` INT(11) NOT NULL DEFAULT 0  
, ADD INDEX `fk_session_address1` (`address_id` ASC) ;

ALTER TABLE `donkeystats`.`source_has_file` CHANGE COLUMN `first_seen` `first_seen` DATETIME NOT NULL  ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

ALTER TABLE source DROP COLUMN version;

ALTER TABLE source DROP COLUMN availability;

ALTER TABLE source CHANGE COLUMN so osinfo VARCHAR(45);

ALTER TABLE source_has_file ADD COLUMN availability DECIMAL(3,2);
