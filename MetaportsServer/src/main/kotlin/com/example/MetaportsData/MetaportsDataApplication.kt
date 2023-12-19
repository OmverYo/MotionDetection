package com.example.MetaportsData

import jakarta.persistence.*
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.web.bind.annotation.*

@SpringBootApplication
class MetaportsDataApplication

fun main(args: Array<String>) {
	runApplication<MetaportsDataApplication>(*args)
}

interface GameDataRepository: JpaRepository<mt_training_result, Int>
{

}

interface PlayerDataRepository: JpaRepository<player_data, Int>
{

}

interface BackgroundDataRepository: JpaRepository<background, Int>
{

}

interface ProgramDataRepository: JpaRepository<program_running, Int>
{

}

interface HandDataRepository: JpaRepository<hand, Int>
{

}

@RestController
@RequestMapping("api")
class GameDataRestController(val GameDataRepo: GameDataRepository)
{
	@GetMapping("GameData")
	fun GetAll() = GameDataRepo.findAll().last()

	@PostMapping("GameData")
	fun SaveGameData(@RequestBody GameData: mt_training_result)
	{
		GameDataRepo.save(GameData)
	}
}

@RestController
@RequestMapping("api")
class PlayerDataRestController(val PlayerDataRepo: PlayerDataRepository)
{
	@GetMapping("PlayerData")
	fun GetAll() = PlayerDataRepo.findAll().last()

	@PostMapping("PlayerData")
	fun SavePlayerData(@RequestBody PlayerData: player_data)
	{
		PlayerDataRepo.save(PlayerData)
	}
}

@RestController
@RequestMapping("api")
class BackgroundDataRestController(val BackgroundDataRepo: BackgroundDataRepository)
{
	@GetMapping("BackgroundData")
	fun GetAll() = BackgroundDataRepo.findAll().last()

	@PostMapping("BackgroundData")
	fun SaveBackgroundData(@RequestBody BackgroundData: background)
	{
		BackgroundDataRepo.save(BackgroundData)
	}
}

@RestController
@RequestMapping("api")
class ProgramDataRestController(val ProgramDataRepo: ProgramDataRepository)
{
	@GetMapping("ProgramData")
	fun GetAll() = ProgramDataRepo.findAll().last()

	@PostMapping("ProgramData")
	fun SaveProgramData(@RequestBody ProgramData: program_running)
	{
		ProgramDataRepo.save(ProgramData)
	}
}

@RestController
@RequestMapping("api")
class HandDataRestController(val HandDataRepo: HandDataRepository)
{
	@GetMapping("HandData")
	fun GetAll() = HandDataRepo.findAll().last()

	@PostMapping("HandData")
	fun SaveHandData(@RequestBody HandData: hand)
	{
		HandData.hand_id = 1
		HandDataRepo.save(HandData)
	}
}

@Entity
class mt_training_result(
	@Id @GeneratedValue(strategy = GenerationType.IDENTITY)
	var play_id: Int = 0,
	var capture_time: Int = 0,
	var accuracy: Int = 0
)

@Entity
class player_data(
	@Id @GeneratedValue(strategy = GenerationType.IDENTITY)
	var play_id: Int = 0,
	var total: Int = 0,
	var perfect_frame: Int = 0,
	var awesome_frame: Int = 0,
	var good_frame: Int = 0,
	var ok_frame: Int = 0,
	var bad_frame: Int = 0
)

@Entity
class background(
	@Id @GeneratedValue(strategy = GenerationType.IDENTITY)
	var user_id: Int = 0,
	var is_vr: Boolean = false,
	var bg_name: String = "",
	var coord_name: String = ""
)

@Entity
class program_running(
	@Id @GeneratedValue(strategy = GenerationType.IDENTITY)
	var program_id: Int = 0,
	var is_running: Boolean = true
)

@Entity
class hand(
	@Id
	var hand_id: Int = 1,
	var rx: Int = 0,
	var ry: Int = 0,
	var lx: Int = 0,
	var ly: Int = 0
)