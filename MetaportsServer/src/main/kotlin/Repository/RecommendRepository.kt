package Repository

import Entity.recommend
import org.springframework.data.jpa.repository.JpaRepository

interface RecommendRepository: JpaRepository<recommend, Int>
{

}