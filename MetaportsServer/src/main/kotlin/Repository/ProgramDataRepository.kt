package Repository

import Entity.program_running
import org.springframework.data.jpa.repository.JpaRepository

interface ProgramDataRepository: JpaRepository<program_running, Int>
{

}
