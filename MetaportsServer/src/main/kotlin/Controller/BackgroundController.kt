package Controller

import Entity.background
import Repository.BackgroundDataRepository
import org.springframework.web.bind.annotation.*

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