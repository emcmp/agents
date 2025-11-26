using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using CrewViewer.Models;

namespace CrewViewer.Pages.Crews
{
    public class ExecutionListModel : PageModel
    {
        private readonly CrewDbContext _context;

        public ExecutionListModel(CrewDbContext context)
        {
            _context = context;
        }

        public Crew? Crew { get; set; }
        public List<Execution> Executions { get; set; } = new();

        public async Task<IActionResult> OnGetAsync(int crewId)
        {
            Crew = await _context.crew.FirstOrDefaultAsync(c => c.id == crewId);

            if (Crew == null)
                return NotFound();

            Executions = await _context.Executions
                .Where(e => e.crew_id == crewId)
                .OrderByDescending(e => e.id)
                .ToListAsync();

            return Page();
        }
    }
}
