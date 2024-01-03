package Controller

import Entity.basic_data
import Repository.BasicDataRepository
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("api")
class BasicDataRestController(val BasicDataRepo: BasicDataRepository)
{
    @GetMapping("BasicData")
    fun GetAll() = BasicDataRepo.findAll().last()

    @PostMapping("BasicData")
    fun SaveBasicData(@RequestBody BasicData: basic_data)
    {
        BasicDataRepo.save(BasicData)
    }
}