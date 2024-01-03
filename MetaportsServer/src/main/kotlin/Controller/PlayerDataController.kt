package Controller

import Entity.player_data
import Repository.PlayerDataRepository
import org.springframework.web.bind.annotation.*

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