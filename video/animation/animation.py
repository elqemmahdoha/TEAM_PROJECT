from matplotlib.animation import FuncAnimation, FFMpegWriter

class TrajetAnimation:
    def __init__(self, trajets, montpellier_graph, compteurs, ax, fig, date_video):
        self.trajets = trajets
        self.montpellier_graph = montpellier_graph
        self.compteurs = compteurs
        self.ax = ax
        self.fig = fig
        self.date_video = date_video
        
        self.frames = max(len(trajet) for trajet in trajets)
        self.start_sizes = [50 for _ in range(len(compteurs))]
        self.sizes = self.start_sizes[:]
        self.p = compteurs['intensity'] / self.frames
        
        self.points, self.lignes = self._initialize_graph_objects()
        self.ax.set_title(f"Date : {self.date_video}")

    def _initialize_graph_objects(self):
        points = []
        lignes = []
        
        point_style = {'color': '#FFFFE0', 'marker': 'o'}
        line_style = {'color': '#FFFF00', 'linewidth': 1}
        
        for _ in self.trajets:
            point, = self.ax.plot([], [], **point_style)
            ligne, = self.ax.plot([], [], **line_style)
            points.append(point)
            lignes.append(ligne)
        
        return points, lignes

    def init(self):
        for point, ligne in zip(self.points, self.lignes):
            point.set_data([], [])
            ligne.set_data([], [])
        return self.points + self.lignes

    def update(self, frame):
        for i, trajet in enumerate(self.trajets):
            if frame < len(trajet):
                x_vals = [self.montpellier_graph.nodes[node]['x'] for node in trajet[:frame + 1]]
                y_vals = [self.montpellier_graph.nodes[node]['y'] for node in trajet[:frame + 1]]
                self.lignes[i].set_data(x_vals, y_vals)
                self.points[i].set_data([self.montpellier_graph.nodes[trajet[frame]]['x']], [self.montpellier_graph.nodes[trajet[frame]]['y']])
            else:
                self.points[i].set_data([], [])

        self.sizes = [size + delta for size, delta in zip(self.sizes, self.p)]
        
        self.compteurs.plot(
            ax=self.ax, 
            marker='o', 
            color='#9b4dca', 
            markersize=self.sizes, 
            alpha=0.2, 
            edgecolor='purple', 
            linewidth=2
        )

        return self.points + self.lignes

    def create_animation(self, output_file, fps=10, bitrate=1800):
        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames=self.frames, 
            init_func=self.init, 
            blit=True, 
            repeat=False
        )
        
        writer = FFMpegWriter(fps=fps, codec='libx264', bitrate=bitrate)
        ani.save(output_file, writer=writer)
