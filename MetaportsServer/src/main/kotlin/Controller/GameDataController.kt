package Controller

import Entity.mt_training_result
import Repository.GameDataRepository
import org.springframework.web.bind.annotation.*

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