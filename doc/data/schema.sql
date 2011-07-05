SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `donkeysurvey` DEFAULT CHARACTER SET latin1 ;
USE `donkeysurvey`;

-- -----------------------------------------------------
-- Table `donkeysurvey`.`file`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeysurvey`.`file` ;

CREATE  TABLE IF NOT EXISTS `donkeysurvey`.`file` (
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
-- Table `donkeysurvey`.`filename`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeysurvey`.`filename` ;

CREATE  TABLE IF NOT EXISTS `donkeysurvey`.`filename` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id` (`id` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1
COMMENT = 'Filenames';


-- -----------------------------------------------------
-- Table `donkeysurvey`.`ed2kuser`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeysurvey`.`ed2kuser` ;

CREATE  TABLE IF NOT EXISTS `donkeysurvey`.`ed2kuser` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `hash` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id` (`id` ASC) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `donkeysurvey`.`connection`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeysurvey`.`connection` ;

CREATE  TABLE IF NOT EXISTS `donkeysurvey`.`connection` (
  `id` BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT ,
  `client_name` VARCHAR(50) NOT NULL ,
  `client_ip` VARCHAR(15) NOT NULL ,
  `client_port` INT(4) NOT NULL ,
  `client_software` VARCHAR(30) NULL ,
  `client_so` VARCHAR(30) NULL ,
  `start_date` DATETIME NOT NULL ,
  `end_date` DATETIME NULL ,
  `total_transferred` INT NOT NULL DEFAULT 0 ,
  `is_download` TINYINT(1) NOT NULL ,
  `availability` DECIMAL(3,2) NULL DEFAULT 0.00 ,
  `ed2kuser_id` BIGINT(20) UNSIGNED NOT NULL ,
  `file_id` BIGINT(20) UNSIGNED NOT NULL ,
  UNIQUE INDEX `id` (`id` ASC) ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_connection_ed2kuser1` (`ed2kuser_id` ASC) ,
  INDEX `fk_connection_file1` (`file_id` ASC) ,
  CONSTRAINT `fk_connection_ed2kuser1`
    FOREIGN KEY (`ed2kuser_id` )
    REFERENCES `donkeysurvey`.`ed2kuser` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_connection_file1`
    FOREIGN KEY (`file_id` )
    REFERENCES `donkeysurvey`.`file` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1
COMMENT = 'Keep sessions information';


-- -----------------------------------------------------
-- Table `donkeysurvey`.`file_has_filename`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `donkeysurvey`.`file_has_filename` ;

CREATE  TABLE IF NOT EXISTS `donkeysurvey`.`file_has_filename` (
  `file_id` BIGINT(20) UNSIGNED NOT NULL ,
  `filename_id` BIGINT(20) UNSIGNED NOT NULL ,
  PRIMARY KEY (`file_id`, `filename_id`) ,
  INDEX `fk_file_has_filename_file1` (`file_id` ASC) ,
  INDEX `fk_file_has_filename_filename1` (`filename_id` ASC) ,
  CONSTRAINT `fk_file_has_filename_file1`
    FOREIGN KEY (`file_id` )
    REFERENCES `donkeysurvey`.`file` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_file_has_filename_filename1`
    FOREIGN KEY (`filename_id` )
    REFERENCES `donkeysurvey`.`filename` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
