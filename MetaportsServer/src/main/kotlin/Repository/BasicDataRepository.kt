package Repository

import Entity.basic_data
import org.springframework.data.jpa.repository.JpaRepository


interface BasicDataRepository: JpaRepository<basic_data, Int>
{

}