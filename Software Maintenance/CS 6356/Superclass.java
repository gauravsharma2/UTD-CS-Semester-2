public class Circle : IDrawable
{
  public Point Center { get; private set; }
  public Color MyColor { get; private set; }
  public int Radius { get; private set; }
  public void Draw()
  {
    // draw...
  }
}

public interface IDrawable
{
  void Draw();
}