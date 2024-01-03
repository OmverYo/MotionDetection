package Controller

import Entity.hand
import Repository.HandDataRepository
import org.springframework.web.bind.annotation.*

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