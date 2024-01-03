package Controller

import Entity.recommend
import Repository.RecommendRepository
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("api")
class RecommendRestController(val RecommendRepo: RecommendRepository)
{
    @GetMapping("Recommend")
    fun GetAll() = RecommendRepo.findAll().last()

    @PostMapping("Recommend")
    fun SaveRecommend(@RequestBody Recommend: recommend)
    {
        RecommendRepo.save(Recommend)
    }
}