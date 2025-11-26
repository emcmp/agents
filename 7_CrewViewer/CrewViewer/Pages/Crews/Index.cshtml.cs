using System.Collections.Generic;
using System.Threading.Tasks;
using CrewViewer.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;

namespace CrewViewer.Pages.Crews
{
    public class IndexModel : PageModel
    {
        private readonly CrewDbContext _context;
        public int exec_count { get; set; }

        public IndexModel(CrewDbContext context)
        {
            _context = context;
        }

        // La liste de crews que la page va afficher
        public IList<Crew> Crews { get; set; } = new List<Crew>();

        public async Task OnGetAsync()
        {
            // Charge tous les crews + agents + tasks
            Crews = await _context.crew
                .Include(c => c.crew_agents)
                    .ThenInclude(ca => ca.agent)
                .Include(c => c.crew_tasks)
                    .ThenInclude(ct => ct.task)
                .ToListAsync();

            foreach (var c in Crews)
            {
                c.exec_count = _context.Executions.Count(e => e.crew_id == c.id);
            }

        }
    }
}
