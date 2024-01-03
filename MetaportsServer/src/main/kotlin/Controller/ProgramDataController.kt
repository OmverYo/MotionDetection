package Controller

import Entity.program_running
import Repository.ProgramDataRepository
import org.springframework.web.bind.annotation.*

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