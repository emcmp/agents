using System.Collections.Generic;
using System.Threading.Tasks;
using CrewViewer.Models;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using System;

namespace CrewViewer.Pages.Crews
{
    public class IndexModel : PageModel
    {
        private readonly CrewDbContext _context;
        private readonly ILogger<IndexModel> _logger;

        public IndexModel(CrewDbContext context, ILogger<IndexModel> logger)
        {
            _context = context;
            _logger = logger;
        }

        // La liste de crews que la page va afficher
        public IList<Crew> Crews { get; set; } = new List<Crew>();

        public async Task OnGetAsync()
        {
            try
            {
                // Charge tous les crews + agents + tasks
                Crews = await _context.crew
                    .Include(c => c.crew_agents)
                        .ThenInclude(ca => ca.agent)
                    .Include(c => c.crew_tasks)
                        .ThenInclude(ct => ct.task)
                    .AsNoTracking() // Performance: pas besoin de tracking pour lecture seule
                    .ToListAsync();

                foreach (var c in Crews)
                {
                    c.exec_count = await _context.Executions
                        .CountAsync(e => e.crew_id == c.id);
                }

                _logger.LogInformation("Successfully loaded {Count} crews", Crews.Count);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading crews list");
                Crews = new List<Crew>();
            }
        }
    }
}
