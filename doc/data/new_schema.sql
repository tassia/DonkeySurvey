SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `donkeystats` DEFAULT CHARACTER SET latin1 ;
USE `donkeystats`;

-- -----------------------------------------------------
-- Table `donkeystats`.`file`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeystats`.`file` ;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`file` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hash` VARCHAR(100) NOT NULL ,
  `size` INT(14) NOT NULL ,
  `partial_size` INT(14) NOT NULL ,
  `best_name` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id` (`id` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `donkeystats`.`filename`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeystats`.`filename` ;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`filename` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id` (`id` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1
COMMENT = 'Filenames';


-- -----------------------------------------------------
-- Table `donkeystats`.`source`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeystats`.`source` ;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`source` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(200) NULL ,
  `hash` VARCHAR(512) NULL ,
  `software` VARCHAR(45) NULL ,
  `version` VARCHAR(45) NULL ,
  `so` VARCHAR(45) NULL ,
  `availability` DECIMAL(2,1) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `donkeystats`.`session`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeystats`.`session` ;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`session` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `ip` VARCHAR(15) NOT NULL ,
  `port` INT(4) NOT NULL ,
  `start_date` DATETIME NOT NULL ,
  `last_update` DATETIME NULL ,
  `downloaded` INT NOT NULL DEFAULT 0 ,
  `uploaded` INT NULL DEFAULT 0 ,
  `file_id` BIGINT(20) UNSIGNED NOT NULL ,
  `source_id` INT NOT NULL ,
  UNIQUE INDEX `id` (`id` ASC) ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_connection_file1` (`file_id` ASC) ,
  INDEX `fk_session_source1` (`source_id` ASC) ,
  CONSTRAINT `fk_connection_file1`
    FOREIGN KEY (`file_id` )
    REFERENCES `donkeystats`.`file` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_source1`
    FOREIGN KEY (`source_id` )
    REFERENCES `donkeystats`.`source` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1
COMMENT = 'Keep sessions information';


-- -----------------------------------------------------
-- Table `donkeystats`.`file_has_filename`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeystats`.`file_has_filename` ;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`file_has_filename` (
  `file_id` BIGINT(20) UNSIGNED NOT NULL ,
  `filename_id` BIGINT(20) UNSIGNED NOT NULL ,
  PRIMARY KEY (`file_id`, `filename_id`) ,
  INDEX `fk_file_has_filename_file1` (`file_id` ASC) ,
  INDEX `fk_file_has_filename_filename1` (`filename_id` ASC) ,
  CONSTRAINT `fk_file_has_filename_file1`
    FOREIGN KEY (`file_id` )
    REFERENCES `donkeystats`.`file` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_file_has_filename_filename1`
    FOREIGN KEY (`filename_id` )
    REFERENCES `donkeystats`.`filename` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `donkeystats`.`source_has_file`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeystats`.`source_has_file` ;

CREATE  TABLE IF NOT EXISTS `donkeystats`.`source_has_file` (
  `source_id` BIGINT(20) UNSIGNED NOT NULL ,
  `file_id` BIGINT(20) UNSIGNED NOT NULL ,
  `first_seen` DATETIME NULL ,
  PRIMARY KEY (`source_id`, `file_id`) ,
  INDEX `fk_source_has_file_source1` (`source_id` ASC) ,
  INDEX `fk_source_has_file_file1` (`file_id` ASC) ,
  CONSTRAINT `fk_source_has_file_source1`
    FOREIGN KEY (`source_id` )
    REFERENCES `donkeystats`.`source` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_source_has_file_file1`
    FOREIGN KEY (`file_id` )
    REFERENCES `donkeystats`.`file` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
